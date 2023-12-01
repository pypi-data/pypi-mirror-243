"""
Configure general settings for your application like the icons to use, how to sync data with the server, and more.
"""
from cave_utils.api_utils.validator_utils import *
import type_enforced


@type_enforced.Enforcer
class settings(ApiValidator):
    """
    The settings are located under the path **`settings`**.
    """

    @staticmethod
    def spec(
        iconUrl: str,
        demo: dict = dict(),
        sync: dict = dict(),
        time: dict = dict(),
        defaults: dict = dict(),
        debug: bool = False,
        **kwargs,
    ):
        """
        Arguments:

        * **`iconUrl`**: `[str]` &rarr; The URL to the icon bundle for your application.
            * **Example**: `"https://react-icons.mitcave.com/4.10.1"`.
            * **Note**: This is the only required attribute in `settings`.
        * **`demo`**: `[dict]` = `{}` &rarr; Settings for the demo mode of your application.
            * **See**: `settings_demo`.
        * **`sync`**: `[dict]` = `{}` &rarr; Settings for syncing data with the server.
            * **See**: `settings_sync`.
        * **`time`**: `[dict]` = `{}` &rarr; Settings for the time display.
            * **See**: `settings_time`.
        * **`defaults`**: `[dict]` = `{}` &rarr; Default settings for your application.
            * **See**: `settings_defaults`.
        * **`debug`**: `[dict]` = `{}` &rarr; If `True`, the CAVE App client will show additional information for debugging purposes.
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        self.__check_url_valid__(
            url=self.data.get("iconUrl"),
        )
        CustomKeyValidator(
            data=self.data.get("sync", {}),
            log=self.log,
            prepend_path=["sync"],
            validator=settings_sync,
            **kwargs,
        )
        CustomKeyValidator(
            data=self.data.get("demo", {}),
            log=self.log,
            prepend_path=["demo"],
            validator=settings_demo,
            **kwargs,
        )
        if self.data.get("time"):
            settings_time(
                data=self.data.get("time", {}),
                log=self.log,
                prepend_path=["time"],
                **kwargs,
            )
        settings_defaults(
            data=self.data.get("defaults", {}),
            log=self.log,
            prepend_path=["defaults"],
            **kwargs,
        )


@type_enforced.Enforcer
class settings_defaults(ApiValidator):
    """
    The defaults settings are located under the path **`settings.defaults`**.
    """

    @staticmethod
    def spec(
        showToolbar: bool = True,
        locale: str = "en-US",
        precision: int = 2,
        trailingZeros: bool = False,
        notation: [str, None] = "standard",
        notationDisplay: [str, None] = None,
        fallbackValue: [str, None] = "N/A",
        unit: [str, None] = None,
        unitPlacement: str = "afterWithSpace",
        legendPrecision: [str, None] = None,
        legendNotation: [str, None] = "standard",
        legendNotationDisplay: [str, None] = None,
        legendMinLabel: [str, None] = None,
        legendMaxLabel: [str, None] = None,
        **kwargs,
    ):
        """
        Arguments:

        * **`showToolbar`**: `[bool]` = `True` &rarr; If `True`, chart toolbars will be displayed by default.
        * **`locale`**: `[str]` = `"en-US"` &rarr;
            * Format numeric values based on language and regional conventions.
            * **Note**: This attribute only applies to `"num"` props.
            * **See**: [Locale identifier][].
        * **`precision`**: `[int]` = `2` &rarr; The number of decimal places to display.
            * **Notes**:
                * Set the precision to `0` to attach an integer constraint.
                * This attribute only applies to `"num"` props.
        * **`trailingZeros`**: `[bool]` = `False` &rarr; If `True`, trailing zeros will be displayed.
            * **Notes**:
                * This ensures that all precision digits are shown. For example: `1.5` &rarr; `1.500` when precision is `3`.
                * This attribute only applies to `"num"` props.
        * **`notation`**: `[int]` = `"standard"` &rarr; The formatting style of a numeric value.
        * **`notationDisplay`**: `[str]` = `"e+"` | `"short"` | `None` &rarr; Further customize the formatting within the selected `notation`.
            * **Notes**:
                * No `notationDisplay` option is provided for a `"standard"` notation
                * The options `"short"` and `"long"` are only provided for the `"compact"` notation
                * The options `"e"`, `"e+"`, `"E"`, `"E+"`, `"x10^"`, and `"x10^+"` are provided for the `"scientific"` and `"engineering"` notations
                * If `None`, it defaults to `"short"` for `"compact"` notation, and to `"e+"` for `"scientific"` or `"engineering"` notations; if the option is set to `"standard"`, its value remains `None`.
                * This attribute only applies to `"num"` props.
        * **`fallbackValue`**: [str] = `"N/A"` &rarr; A value to show when a numeric value is missing or invalid.
            * **Note**: This attribute only applies to `"num"` props.
        * **`unit`**: `[str]` = `None` &rarr; The unit to use for a prop or stat.
            * **Note**: This attribute only applies to `"num"` props.
        * **`unitPlacement`**: `[str]` = `"afterWithSpace"` &rarr; The position of the `unit` symbol relative to a value.
            * **Accepted Values**:
                * `"after"`: The `unit` appears after the value.
                * `"afterWithSpace"`: The `unit` appears after the value, separated by a space.
                * `"before"`: The `unit` appears before the value.
                * `"beforeWithSpace"`: The unit is placed before the value, with a space in between.
            * **Note**: This attribute only applies to `"num"` props.
        * **`legendPrecision`**: `[int]` = `None` &rarr;
            * The number of decimal places to display in the Map Legend.
            * **Notes**:
                * Set the precision to `0` to attach an integer constraint.
                * If left unspecified (i.e. `None`), the prop's `precision` will be used or in case the latter is undefined, `settings.precision` will be used.
                * This attribute only applies to `"num"` props.
        * **`legendNotation`**: `[int]` = `"standard"` &rarr; The formatting style of a numeric value.
            * **Accepted Values**:
                * `"standard"`: Plain number formatting
                * `"compact"`: Resembles the [metric prefix][] system
                * `"scientific"`: [Scientific notation][]
                * `"engineering"`: [Engineering notation][]
            * **Notes**:
                * If left unspecified (i.e. `None`), the prop's `notation` will be used or in case the latter is undefined, `settings.notation` will be used.
                * This attribute only applies to `"num"` props.
        * **`legendNotationDisplay`**: `[str]` = `"e+"` | `"short"` | `None` &rarr; Further customize the formatting within the selected `legendNotation`.
            * **Accepted Values**:
                * `"short"`: Add symbols `K`, `M`, `B`, and `T` (in `"en-US"`) to denote thousands, millions, billions, and trillions, respectively.
                * `"long"`: Present numeric values with the informal suffix words `thousand`, `million`, `billion`, and `trillion` (in `"en-US"`).
                * `"e"`: Exponent symbol in lowercase as per the chosen `locale` identifier
                * `"e+"`: Similar to `"e"`, but with a plus sign for positive exponents.
                * `"E"`: Exponent symbol in uppercase as per the chosen `locale` identifier
                * `"E+"`: Similar to `"E"`, but with a plus sign for positive exponents.
                * `"x10^"`: Formal scientific notation representation
                * `"x10^+"`: Similar to `"x10^"`, with a plus sign for positive exponents.
            * **Notes**:
                * No `legendNotationDisplay` option is provided for a `"standard"` legend notation
                * The options `"short"` and `"long"` are only provided for the `"compact"` legend notation
                * The options `"e"`, `"e+"`, `"E"`, `"E+"`, `"x10^"`, and `"x10^+"` are provided for the `"scientific"` and `"engineering"` legend notations
                * If left unspecified (i.e. `None`), the prop's `notationDisplay` will be used or in case the latter is undefined, `settings.notationDisplay` will be used.
                * This attribute only applies to `"num"` props.
        * **`legendMinLabel`**: `[str]` = `None` &rarr;
            * A custom and descriptive label in the Map Legend used to identify the lowest data point.
            * **Notes**:
                * Takes precedence over other formatting, except when used in a node cluster and the `cave_utils.api.maps.group` attribute is `True`. In this case, the min value within the node cluster is displayed.
                * This attribute only applies to `"num"` props.
        * **`legendMaxLabel`**: `[str]` = `None` &rarr;
            * A custom and descriptive label in the Map Legend used to identify the highest data point.
            * **Notes**:
                * Takes precedence over other formatting, except when used in a node cluster and the `cave_utils.api.maps.group` attribute is `True`. In this case, the max value within the node cluster is displayed.
                * This attribute only applies to `"num"` props.

        [locale identifier]: https://en.wikipedia.org/wiki/IETF_language_tag
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {
                "unitPlacement": ["after", "afterWithSpace", "before", "beforeWithSpace"],
                # TODO: Validate
                # compact: allowed notation displays -> "short", "long"
                # scientific|engineering: allowed notation displays -> "e", "e+", "E", "E+", "x10^", "x10^+"
                # standard: allowed notation displays -> None
                "notation": ["compact", "precision", "scientific"],
                "notationDisplay": ["short", "long", "e", "e+", "E", "E+", "x10^", "x10^+"],
                "legendNotation": ["compact", "precision", "scientific"],
                "legendNotationDisplay": ["short", "long", "e", "e+", "E", "E+", "x10^", "x10^+"],
            },
        }


@type_enforced.Enforcer
class settings_demo(ApiValidator):
    """
    The demo settings are located under the path **`settings.demo`**.
    """

    @staticmethod
    def spec(scrollSpeed: [int, float] = 1, displayTime: int = 5, **kwargs):
        """
        Arguments:

        * **`scrollSpeed`**: `[int, float]` = `1` &rarr;
            * The speed at which the demo text will scroll, measured in degrees of rotation per frame (degrees per 13 milliseconds).
            * **Note**: This key only applies to `"map"` charts.
        * **`displayTime`**: `[int]` = `5` &rarr; The time duration in seconds to display the demo text.
        """
        return {"kwargs": kwargs, "accepted_values": {}}


@type_enforced.Enforcer
class settings_sync(ApiValidator):
    """
    The sync settings are located under the path **`settings.sync`**.
    """

    @staticmethod
    def spec(name: str, showToggle: bool, value: bool, data: dict, **kwargs):
        """
        Arguments:

        * **`name`**: `[str]` &rarr; The name of the sync setting.
        * **`showToggle`**: `[bool]` &rarr; If `True`, the toggle will be displayed.
        * **`value`**: `[bool]` &rarr; The initial value of the toggle.
        * **`value`**: `[dict]` &rarr; The data to sync with the server.
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    # def __extend_spec__(self, **kwargs):
    #     root_data = kwargs.get("root_data", {})
    #     for key, path in self.data.get("data", {}).items():
    #         if not pamda.hasPath(path, root_data):
    #             self.__warn__(f"Path {path} does not exist.", prepend_path=["data", key])


@type_enforced.Enforcer
class settings_time(ApiValidator):
    """
    The time settings are located under the path **`settings.time`**.
    """

    @staticmethod
    def spec(timeLength: int, timeUnits: str, **kwargs):
        """
        Arguments:

        * **`timeLength`**: `[int]` &rarr; The amount of time values to display.
        * **`timeUnits`**: `[str]` &rarr; The units of time to display.
            * **Example**: `"Decade"`.
        """
        return {"kwargs": kwargs, "accepted_values": {}}
