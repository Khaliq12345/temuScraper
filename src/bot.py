import asyncio
from temu_captcha_solver.launcher import make_nodriver_solver
from playwright.sync_api import sync_playwright, Page
from temu_captcha_solver import make_playwright_solver_context
from temu_captcha_solver.playwrightsolver import expect
from src.database_manager import save_data, update_process_status
from src.parser import extract_goods_from_html
from src import config


def process_page(page: Page, click_number: int) -> None:
    """Click through all pages and extract data"""
    for i in range(click_number):
        try:
            show_more = page.get_by_role("button", name="See more")
            if not show_more.is_visible():
                print("No Show More Button !")
                break
            show_more.scroll_into_view_if_needed(timeout=5000)
            show_more.click()
            print(f"Clicked Now {i + 1} Time")
            page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Error - {e}")

    # parser html and save data
    page_html = page.content()
    goods_list = extract_goods_from_html(page_html)
    save_data(goods_list)
    print("Scraping Ended")


def login(page: Page):
    print("Logging into the Temu")
    page.get_by_role("textbox", name="Email or phone number").fill(
        config.EMAIL, timeout=60000
    )
    page.get_by_role("button", name="Continue").click()
    page.screenshot(path="image.png")
    page.get_by_role("textbox", name="Password").fill(
        config.PASSWORD, timeout=60000
    )
    page.get_by_role("button", name="Sign in").click()


def check_and_solve_captcha(page: Page):
    print("Solving Captcha")
    page.wait_for_timeout(10000)

    expect(page.get_by_text("Security Verification")).to_be_hidden(
        timeout=120000
    )
    print("Captcha is hidden/solved")


def human_wait(page: Page):
    print("Waiting..")
    page.wait_for_load_state(state="load", timeout=120000)
    page.wait_for_timeout(5000)
    print("Waiting done")


def run(url: str, click_number: int) -> None:
    with sync_playwright() as p:
        # setup browser with captcha plugin
        browser = p.chromium.launch(headless=False)
        context = make_playwright_solver_context(
            p,
            config.CAPTCHA_KEY,
            headless=False,
            viewport={"width": 1280, "height": 800},
            is_mobile=True,
        )

        # login into Temu
        page = context.new_page()
        page.goto("https://www.temu.com/", timeout=60000)

        # accept cookies
        try:
            page.get_by_role("button", name="Accept all").click(timeout=30000)
        except Exception as e:
            print(f"Cookie not found - {e}")

        check_and_solve_captcha(page)
        human_wait(page)

        # page.get_by_role("searchbox", name="women hot clothes").click()
        page.get_by_role("searchbox").fill("games")
        page.get_by_role("button", name="Submit search").click()

        human_wait(page)

        # login(page)
        #
        # check_and_solve_captcha(page)
        #
        # print("Going to the listing page")
        # page.goto(url, timeout=60000)
        # check_and_solve_captcha(page)

        print("Starting Process")
        process_page(page, click_number)

        # close the browser
        browser.close()


def main(url: str, click_number: int, process_id: str) -> None:
    update_process_status(process_id, "running")
    try:
        run(url, click_number)
        update_process_status(process_id, "success")
    except Exception as e:
        update_process_status(process_id, "failed")
        print(f"Error - {e}")
