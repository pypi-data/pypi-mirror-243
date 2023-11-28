import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from ipaddress import IPv4Address
from multiprocessing.pool import ThreadPool
from threading import Thread
from typing import Callable, Dict, List, Union

from jarvis.executors import files, internet
from jarvis.executors import lights_squire as squire
from jarvis.executors import word_match
from jarvis.modules.audio import speaker
from jarvis.modules.conditions import conversation
from jarvis.modules.lights import preset_values
from jarvis.modules.logger import logger
from jarvis.modules.models import models
from jarvis.modules.utils import support, util


def get_lights(data: dict) -> Dict[str, Union[List[str], List[List[str]]]]:
    """Extract lights' mapping from the data in smart devices.

    Args:
        data: Raw data from smart devices.

    Returns:
        Dict[str, Union[List[str], List[List[str]]]]:
        Return lights' information and the key name under which it was stored. The key will be used to update the file.
    """
    for key, value in data.items():
        if key.lower() in ("light", "lights"):
            return data[key]


class ThreadExecutor:
    """Instantiates ``ThreadExecutor`` object to control the lights using pool of threads.

    >>> ThreadExecutor

    """

    def __init__(self, host_ip: List[str], mapping: Dict[str, List[List[str]]]):
        """Initializes the class and assign object members."""
        self.host_ip = host_ip
        self.mapping = mapping

    def thread_worker(self, function_to_call: Callable) -> List[str]:
        """Initiates ``ThreadPoolExecutor`` with in a dedicated thread.

        Args:
            function_to_call: Takes the function/method that has to be called as an argument.
        """
        futures = {}
        executor = ThreadPoolExecutor(max_workers=len(self.host_ip))
        with executor:
            for iterator in self.host_ip:
                future = executor.submit(function_to_call, iterator)
                futures[future] = iterator

        thread_except = []
        for future in as_completed(futures):
            if future.exception():
                thread_except.append(futures[future])
                logger.error("Thread processing for '%s' received an exception: %s", iterator, future.exception())
        return thread_except

    def avail_check(self, function_to_call: Callable) -> None:
        """Speaks an error message if any of the lights aren't reachable.

        Args:
            function_to_call: Takes the function/method that has to be called as an argument.
        """
        status = ThreadPool(processes=1).apply_async(func=self.thread_worker, args=[function_to_call])
        speaker.speak(run=True)  # Speak the initial response when the work is happening behind the scenes
        if failed := status.get(timeout=5):
            any_in = lambda a, b: bool(set(a).intersection(b))  # noqa: E731
            failed_msg = []
            for k, v in self.mapping.items():
                if any_in(a=failed, b=v):
                    if failed_msg:
                        failed_msg.append(f'{support.pluralize(count=len(v), word="light", to_words=True)} from {k}')
                    else:
                        failed_msg.append(
                            f'{support.pluralize(count=len(v), word="light", to_words=True, cap_word=True)} from {k}')
            if len(failed_msg) == 1 and failed_msg[0].startswith('One'):  # Failed only on a single lamp
                response = "".join(failed_msg) + " isn't available right now!"
            else:
                response = util.comma_separator(list_=failed_msg) + " aren't available right now!"
            logger.error(response)
            speaker.speak(text=f"I'm sorry {models.env.title}! {response}")


def lights(phrase: str) -> None:
    """Controller for smart lights.

    Args:
        phrase: Takes the phrase spoken as an argument.
    """
    if not internet.vpn_checker():
        return

    smart_devices = files.get_smart_devices()
    if smart_devices is False:
        speaker.speak(text=f"I'm sorry {models.env.title}! I wasn't able to read the source information.")
        return
    if smart_devices and (lights_map := get_lights(data=smart_devices)):
        logger.debug(lights_map)
    else:
        logger.warning("%s is empty for lights.", models.fileio.smart_devices)
        support.no_env_vars()
        return

    phrase = phrase.lower()

    if 'all' in phrase.split():
        light_location = ""
        if "except" in phrase or "exclud" in phrase:
            remove = util.matrix_to_flat_list(input_=squire.word_map.values()) + ['lights', 'light']
            phrase_location = phrase
            for word in remove:
                phrase_location = phrase_location.replace(word, '')
            exclusion = util.get_closest_match(text=phrase_location.strip(), match_list=list(lights_map.keys()))
            host_names: List[List[str]] = util.remove_duplicates(
                input_=util.matrix_to_flat_list([lights_map[light] for light in lights_map if light != exclusion])
            )
            logger.debug("%d lights' excluding %s", len(host_names), exclusion)
        else:
            host_names: List[str] = util.remove_duplicates(
                input_=util.matrix_to_flat_list(input_=[v for k, v in lights_map.items()])
            )
            logger.debug("All lights: %d", len(host_names))
    else:
        remove = util.matrix_to_flat_list(input_=squire.word_map.values()) + ['lights', 'light']
        phrase_location = phrase
        for word in remove:
            phrase_location = phrase_location.replace(word, '')
        light_location = util.get_closest_match(text=phrase_location.strip(), match_list=list(lights_map.keys()))
        host_names: List[str] = lights_map[light_location]
        logger.info("%d lights' location: %s", len(host_names), light_location)
    host_names = util.remove_none(input_=host_names)
    if light_location and not host_names:
        logger.warning("No hostname values found for %s in %s", light_location, models.fileio.smart_devices)
        speaker.speak(text=f"I'm sorry {models.env.title}! You haven't mentioned the host names of {light_location!r} "
                           "lights.")
        return
    if not host_names:
        Thread(target=support.unrecognized_dumper, args=[{'LIGHTS': phrase}]).start()
        speaker.speak(text=f"I'm not sure which lights you meant {models.env.title}!")
        return

    # extract IP addresses for hostnames that are required
    for _light_location, _light_hostname in lights_map.items():
        lights_map[_light_location] = []
        for hostname in _light_hostname:
            if hostname in host_names:
                if resolved := support.hostname_to_ip(hostname=hostname):
                    logger.debug("Resolved IP %s for hostname %s", resolved, hostname)
                else:
                    logger.error("Unable to resolve IP for %s", hostname)
                    resolved = [IPv4Address("0.0.0.0")]  # Add placeholder IP to respond accordingly
                lights_map[_light_location].extend(list(map(str, resolved)))
    host_ip = util.matrix_to_flat_list(input_=util.remove_none(input_=list(lights_map.values())))
    # host_ip = util.matrix_to_flat_list(input_=util.remove_none(input_=host_ip))  # in case of multiple matrix
    if not host_ip:
        plural = 'lights' if len(host_names) > 1 else 'light'
        light_location = light_location.replace('_', ' ').replace('-', '')
        speaker.speak(text=f"I wasn't able to connect to your {light_location} {plural} {models.env.title}! "
                           f"{support.number_to_words(input_=len(host_names), capitalize=True)} {plural} appear to be "
                           "powered off.")
        return
    host_ip = util.remove_duplicates(host_ip)
    executor = ThreadExecutor(host_ip=host_ip, mapping=lights_map)

    plural = 'lights' if len(host_ip) > 1 else 'light'
    if word_match.word_match(phrase, squire.word_map['turn_on']):
        tone = 'white' if 'white' in phrase else 'cool'
        if 'turn on' in phrase:
            speaker.speak(text=f'{random.choice(conversation.acknowledgement)}! Turning on {len(host_ip)} {plural}')
        else:
            speaker.speak(
                text=f'{random.choice(conversation.acknowledgement)}! Setting {len(host_ip)} {plural} to {tone}!'
            )
        executor.avail_check(function_to_call=squire.cool)
    elif word_match.word_match(phrase, squire.word_map['turn_off']):
        speaker.speak(text=f'{random.choice(conversation.acknowledgement)}! Turning off {len(host_ip)} {plural}')
        if state := squire.check_status():
            support.stop_process(pid=int(state[0]))
        if word_match.word_match(phrase, squire.word_map['reset']):
            Thread(target=executor.thread_worker, args=[squire.cool]).run()
        executor.avail_check(function_to_call=squire.turn_off)
    elif word_match.word_match(phrase, squire.word_map['party_mode']):
        if squire.party_mode(host=host_ip, phrase=phrase):
            Thread(target=executor.thread_worker, args=[squire.cool]).run()
            Thread(target=executor.thread_worker, args=[squire.turn_off]).start()
    elif word_match.word_match(phrase, squire.word_map['warm']):
        if 'yellow' in phrase:
            speaker.speak(text=f'{random.choice(conversation.acknowledgement)}! '
                               f'Setting {len(host_ip)} {plural} to yellow!')
        else:
            speaker.speak(text=f'Sure {models.env.title}! Setting {len(host_ip)} {plural} to warm!')
        executor.avail_check(function_to_call=squire.warm)
    elif color := word_match.word_match(phrase=phrase, match_list=list(preset_values.PRESET_VALUES.keys())):
        speaker.speak(text=f"{random.choice(conversation.acknowledgement)}! "
                           f"I've changed {len(host_ip)} {plural} to {color}!")
        for light_ip in host_ip:
            squire.preset(host=light_ip, speed=50,
                          color=[preset_values.PRESET_VALUES[_type] for _type in
                                 list(preset_values.PRESET_VALUES.keys()) if _type in phrase][0])
    elif word_match.word_match(phrase, squire.word_map['set']):
        if 'bright' in phrase:
            level = 100
        elif 'dim' in phrase:
            level = 50
        else:
            level = util.extract_nos(input_=phrase, method=int)
            if level is None:
                level = 100
        speaker.speak(text=f"{random.choice(conversation.acknowledgement)}! "
                           f"I've set {len(host_ip)} {plural} to {level}%!")
        level = round((255 * level) / 100)
        Thread(target=executor.thread_worker, args=[squire.turn_off]).run()
        time.sleep(1)
        for light_ip in host_ip:
            squire.lumen(host=light_ip, rgb=level)
    else:
        speaker.speak(text=f"I didn't quite get that {models.env.title}! What do you want me to do to your "
                           f"{light_location} {plural}?")
        Thread(target=support.unrecognized_dumper, args=[{'LIGHTS': phrase}]).start()
