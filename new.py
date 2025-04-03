import os
import time
import re
import subprocess
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 🏁 Step 1: Function to find and launch Geekbench
def get_geekbench_path():
    paths = [
        r"C:\Program Files\Geekbench 6\Geekbench 6.exe",
        r"C:\Program Files (x86)\Geekbench 6\Geekbench 6.exe",
        os.path.join(os.getcwd(), "Geekbench_Windows", "Geekbench 6.exe")
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def launch_geekbench():
    geekbench_path = get_geekbench_path()
    if geekbench_path:
        print("📌 Launching Geekbench...")
        subprocess.Popen([geekbench_path])
        time.sleep(5)  # Give Geekbench some time to load
        return True
    else:
        print("❌ Geekbench is not installed.")
        return False

# 🖱️ Step 2: Click 'Run CPU Benchmark' Button
def click_cpu_benchmark():
    print("🎯 Looking for 'Run CPU Benchmark' button...")
    time.sleep(3)  # Allow time for UI to load

    for attempt in range(5):  # Retry 5 times if needed
        button = pyautogui.locateCenterOnScreen("cpu_benchmark_button.png", confidence=0.8)
        if button:
            pyautogui.click(button)
            print("🚀 CPU Benchmark started!")
            return True
        time.sleep(2)

    print("❌ Could not locate the 'Run CPU Benchmark' button.")
    return False

# ⏳ Step 3: Wait for Benchmark Completion
def wait_for_geekbench():
    print("⏳ Waiting for Geekbench test to complete (Approx. 8 min)...")
    time.sleep(480)  # 8 minutes
    print("✅ Geekbench test completed!")

# 🌍 Step 4: Open Geekbench Result in Chrome
def open_geekbench_browser():
    print("🌍 Opening Chrome to check results...")

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Open Geekbench results page
    driver.get("https://browser.geekbench.com/v6/cpu")
    time.sleep(5)  # Allow page to load

    # Simulate pressing 'CTRL+S' to save the page
    pyautogui.hotkey("ctrl", "s")
    time.sleep(2)

    # Save the page as an HTML file
    save_path = os.path.join(os.getcwd(), "geekbench_result.html")
    pyautogui.typewrite(save_path)
    pyautogui.press("enter")

    print(f"💾 Geekbench result saved as {save_path}")
    driver.quit()
    return save_path

# 📊 Step 5: Extract Scores from the Saved HTML File
def extract_scores_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Extract Single-Core and Multi-Core Scores
    single_core_match = re.search(r"Single-Core Score.*?>(\d+)<", content, re.DOTALL)
    multi_core_match = re.search(r"Multi-Core Score.*?>(\d+)<", content, re.DOTALL)

    if single_core_match and multi_core_match:
        single_core = single_core_match.group(1)
        multi_core = multi_core_match.group(1)
        print(f"✅ Geekbench Results:")
        print(f"🔹 Single-Core Score: {single_core}")
        print(f"🔹 Multi-Core Score: {multi_core}")
    else:
        print("❌ Could not extract scores from the saved HTML file.")

# 🏁 Main Execution
if __name__ == "__main__":
    # Step 1: Launch Geekbench
    if launch_geekbench():
        # Step 2: Click 'Run CPU Benchmark'
        if click_cpu_benchmark():
            # Step 3: Wait for the test to complete
            wait_for_geekbench()
            
            # Step 4: Open Geekbench Result Page in Chrome
            saved_html = open_geekbench_browser()

            # Step 5: Extract & Print Scores
            extract_scores_from_html(saved_html)
