"""
automation.py
Tiny wrapper around Playwright that opens Turbify and performs a couple of actions
(searching a domain and navigating to key sections).

✓ Works headless or with a visible browser window
✓ Detects both available and unavailable domain results
"""

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PWTimeout,
    expect,
)


class TurbifyAutomation:
    def __init__(self, headless: bool = False) -> None:
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        self.page.goto("https://www.turbify.com", timeout=30_000)

    # ------------------------------------------------------------------ #
    # PUBLIC HELPERS
    # ------------------------------------------------------------------ #

    def search_domain(self, domain_name: str) -> str:
        """
        Searches for a domain and returns the availability string.

        Examples of returned strings:
        • "CONGRATS, YOUR DOMAIN IS AVAILABLE!"
        • "Sorry, the domain rosik.com is already registered."
        • "⚠️ Domain result not clearly found"
        """
        self.page.goto("https://www.turbify.com/domains", timeout=30_000)

        # 1️⃣ Wait for the first <input> on the page, then type
        input_box = self.page.locator("//input").first
        expect(input_box).to_be_visible(timeout=10_000)
        input_box.fill(domain_name)

        # 2️⃣ Click the visible “Search” div
        self.page.locator("(//div[normalize-space()='Search'])[1]").click()

        # 3️⃣ Give the page time to update
        try:
            self.page.wait_for_load_state("networkidle", timeout=15_000)
        except PWTimeout:
            pass  # Sometimes results load via XHR without full nav

        # 4️⃣ Grab the result text
        try:
            # ✅ Available case
            available = self.page.locator("(//div[@class='DomainSearchStep-result-available'])[1]")
            if available.is_visible():
                return available.inner_text().strip()

            # ❌ Unavailable case
            unavailable = self.page.locator("(//p[@class='unavailableText'])[1]")
            if unavailable.is_visible():
                return unavailable.inner_text().strip()

            return "⚠️ Domain result not clearly found"
        except Exception as e:  # Catch any locator errors
            return f"⚠️ Error checking domain availability: {str(e)}"

    def choose_hosting_plan(self) -> str:
        """
        Clicks the "Choose Plan" button on the hosting page,
        then returns a fixed message describing Turbify's hosting plans.
        """
        try:
            # Click the "Choose Plan" button
            choose_btn = self.page.locator("(//div[@class='WebHosting-Premiercontainer'])[1]").first
            choose_btn.wait_for(state="visible", timeout=10_000)
            choose_btn.click()

            # Return fixed plans description
            return "Turbify Web Hosting Plans: We have Essentials, Professional, and Advanced."
        except Exception as e:
            return f"⚠️ Could not perform action: {e}"

    def navigate_to(self, section: str) -> str:
        """Navigates the browser to Web Hosting or Domains, and clicks Choose Plan if hosting."""
        section = section.lower()
        if "hosting" in section:
            self.page.goto("https://www.turbify.com/hosting", timeout=30_000)
            # After navigation, click choose plan and get plan description
            plan_msg = self.choose_hosting_plan()
            return f"Navigated to Web Hosting ✔️\n{plan_msg}"

        if "domain" in section:
            self.page.goto("https://www.turbify.com/domains", timeout=30_000)
            return "Navigated to Domains ✔️"

        return "❓ Section not recognized"

    # ------------------------------------------------------------------ #
    # CLEAN‑UP
    # ------------------------------------------------------------------ #

    def close(self) -> None:
        """Closes the Playwright browser cleanly."""
        self.browser.close()
        self.playwright.stop()
