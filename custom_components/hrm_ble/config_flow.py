from homeassistant.config_entries import (ConfigFlow, ConfigFlowResult)
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
import voluptuous as vol

from .const import DOMAIN, CONF_MAC, CONF_TITLE


class HRMBLEConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self.name: str = ""
        self.discovery_name: str = ""
        self.discovery_address: str = ""


    async def async_step_bluetooth(self, discovery_info: BluetoothServiceInfoBleak) -> ConfigFlowResult:
        await self.async_set_unique_id(f"{discovery_info.name}-{discovery_info.address}")
        self._abort_if_unique_id_configured()

        self.discovery_name = discovery_info.name
        self.discovery_address = discovery_info.address
        self.name = f"HRM {discovery_info.name or discovery_info.address}"

        return self.async_show_confirm()


    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        return self.async_show_confirm()


    async def async_step_confirm(self, user_input=None) -> ConfigFlowResult:
        if user_input is None:
            return self.async_show_confirm()

        name = user_input.get(CONF_TITLE, f"HRM {user_input.get(CONF_MAC)}")

        return self.async_create_entry(
            title=name,
            data=user_input
        )


    def async_show_confirm(self) -> ConfigFlowResult:
        schema = vol.Schema(
            {
                vol.Optional(CONF_TITLE, default=self.name): str,
                vol.Required(CONF_MAC, default=self.discovery_address): str,
            }
        )

        return self.async_show_form(
            step_id="confirm",
            data_schema=schema,
        )
