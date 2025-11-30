from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a mobile viewport
        context = browser.new_context(viewport={'width': 375, 'height': 812})
        page = context.new_page()
        
        # Load local index.html
        cwd = os.getcwd()
        page.goto(f"file://{cwd}/index.html")
        
        # Login first (it has login overlay)
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'admin')
        page.click('button[type="submit"]')
        
        # Wait for dashboard
        page.wait_for_selector('#dashboard')
        
        # 1. Verify Sidebar is hidden initially on mobile
        sidebar = page.locator('#sidebar')
        # Check if it has the negative margin (or check visual position)
        # We can check bounding box
        box = sidebar.bounding_box()
        print(f"Initial Sidebar Box: {box}")
        
        # Take screenshot of Initial Mobile View (Bottom Nav should be visible)
        page.screenshot(path="verification_mobile_initial.png")
        
        # 2. Click Hamburger
        page.click('#sidebarCollapse')
        page.wait_for_timeout(500) # Wait for transition
        
        # Sidebar should now be visible (x=0)
        box_active = sidebar.bounding_box()
        print(f"Active Sidebar Box: {box_active}")
        
        page.screenshot(path="verification_mobile_sidebar.png")
        
        # 3. Verify Bottom Nav Items
        nav_text = page.locator('.bottom-navbar').inner_text()
        print(f"Bottom Nav Text: {nav_text}")
        
        # 4. Click User in Bottom Nav
        # Close sidebar first by clicking backdrop
        page.click('#sidebarBackdrop')
        page.wait_for_timeout(500)
        
        # Click User link
        page.click('.bottom-navbar .nav-link:has-text("User")')
        page.wait_for_selector('#profileModal', state='visible')
        
        page.screenshot(path="verification_mobile_profile.png")
        
        browser.close()

if __name__ == "__main__":
    run()
