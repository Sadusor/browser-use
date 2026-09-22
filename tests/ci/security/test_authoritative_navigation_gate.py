import pytest

from browser_use.browser import BrowserProfile, BrowserSession
from browser_use.browser.events import NavigateToUrlEvent
from browser_use.browser.watchdogs.security_watchdog import SecurityWatchdog


@pytest.mark.asyncio
async def test_core_navigation_checks_domain_policy_before_any_browser_effect():
	"""The effect-owning navigation handler must reject before CDP/tab effects."""
	session = BrowserSession(
		browser_profile=BrowserProfile(
			allowed_domains=['localhost'],
			headless=True,
			user_data_dir=None,
		)
	)
	watchdog = SecurityWatchdog(event_bus=session.event_bus, browser_session=session)
	session._security_watchdog = watchdog

	with pytest.raises(ValueError, match='blocked by security policy'):
		await session.on_NavigateToUrlEvent(
			NavigateToUrlEvent(url='http://127.0.0.1:65535/disallowed')
		)

	assert session.agent_focus_target_id is None
	assert session.session_manager is None
