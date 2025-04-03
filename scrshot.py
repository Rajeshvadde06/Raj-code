import os
import time
import subprocess
import pyautogui
import pytesseract
import re
import json
from PIL import Image

# Configure Tesseract-OCR (Ensure Tesseract is installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def get_geekbench_path():
    """Find the installed Geekbench executable path."""
    paths = [
        r"C:\\Program Files\\Geekbench 6\\Geekbench 6.exe",
        r"C:\\Program Files (x86)\\Geekbench 6\\Geekbench 6.exe",
        os.path.join(os.getcwd(), "Geekbench_Windows", "Geekbench 6.exe")
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def launch_geekbench():
    """Launch Geekbench application."""
    geekbench_path = get_geekbench_path()
    if geekbench_path:
        print("📌 Launching Geekbench...")
        subprocess.Popen([geekbench_path])
        time.sleep(5)  # Wait for it to load
        return True
    else:
        print("❌ Geekbench is not installed.")
        return False

def click_cpu_benchmark():
    """Locate and click the 'Run CPU Benchmark' button in Geekbench."""
    print("🎯 Looking for 'Run CPU Benchmark' button...")
    time.sleep(3)  # Allow UI to load

    for _ in range(5):  # Try up to 5 times
        button = pyautogui.locateCenterOnScreen("cpu_benchmark_button.png", confidence=0.8)
        if button:
            pyautogui.click(button.x, button.y)
            print("✅ CPU Benchmark started!")
            return True
        time.sleep(2)

    print("❌ Could not find 'Run CPU Benchmark' button. Make sure the image is correct.")
    return False

def wait_for_geekbench():
    """Wait for the Geekbench test to complete."""
    print("⏳ Waiting for Geekbench test to complete (approx. 8 minutes)...")
    time.sleep(480)  # Wait for ~8 minutes

def take_screenshot():
    """Take a screenshot of the Geekbench results page."""
    screenshot_path = "geekbench_result.png"
    time.sleep(5)  # Wait for the result page to load
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")
    return screenshot_path

def extract_data_from_screenshot(screenshot_path):
    """Extract Page URL, Single-Core Score, and Multi-Core Score from the screenshot."""
    try:
        image = Image.open(screenshot_path)
        extracted_text = pytesseract.image_to_string(image)
        print("📂 Extracted text saved to extracted_text.txt")

        with open("extracted_text.txt", "w", encoding="utf-8") as file:
            file.write(extracted_text)

        print("🔍 Processed Extracted Text:", extracted_text)

        # Extract URL using regex
        url_pattern = r"https?://browser\\.geekbench\\.com/v6/cpu/\\d+"
        match_url = re.search(url_pattern, extracted_text)
        page_url = match_url.group() if match_url else "❌ URL not found"

        # Extract scores using regex (modified to correctly capture both scores)
        score_pattern = r"(\d+)\s+(\d+)\s+Single-Core Score\s+Multi-Core Score"
        match_scores = re.search(score_pattern, extracted_text)

        if match_scores:
            single_core_score = match_scores.group(1)
            multi_core_score = match_scores.group(2)
            print(f"🌐 Page URL: {page_url}")
            print(f"🏆 Scores - Single-Core: {single_core_score}, Multi-Core: {multi_core_score}")
        else:
            print("❌ Scores not found correctly in the image.")
            single_core_score = None
            multi_core_score = None

        # Save extracted data to JSON file
        results = {
            "Page URL": page_url,
            "Single-Core Score": single_core_score,
            "Multi-Core Score": multi_core_score
        }

        with open("geekbench_results.json", "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, indent=4)

        print("📊 Results saved to geekbench_results.json")
        return page_url, single_core_score, multi_core_score

    except Exception as e:
        print(f"❌ Error extracting data: {e}")
        return None, None, None

def main():
    print("🚀 Starting Automated Geekbench Test...")

    # Step 1: Launch Geekbench
    if not launch_geekbench():
        return

    # Step 2: Start CPU Benchmark Test
    if not click_cpu_benchmark():
        return

    # Step 3: Wait for benchmark to complete (~8 minutes)
    wait_for_geekbench()

    # Step 4: Take a screenshot of the results page
    screenshot_path = take_screenshot()

    # Step 5: Extract and display the Geekbench Scores and URL
    page_url, single_core_score, multi_core_score = extract_data_from_screenshot(screenshot_path)

    if page_url or single_core_score or multi_core_score:
        print(f"🌐 Final Results:")
        #print(f"   📄 Page URL: {page_url}")
        print(f"   🏆 Single-Core Score: {single_core_score}")
        print(f"   🔥 Multi-Core Score: {multi_core_score}")
    else:
        print("❌ Failed to extract the necessary information.")

if __name__ == "__main__":
    main()
