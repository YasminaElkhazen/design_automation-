import streamlit as st
from PIL import Image
import easyocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

def extract_names(image):
    # Save the uploaded image to a temporary file to avoid path issues
    temp_image_path = 'temp_image.png'
    image.save(temp_image_path)

    # Use easyocr to do OCR on the image
    results = reader.readtext(temp_image_path)

    # Extract names from the results
    names = [result[1] for result in results]

    return names

def generate_certificate(name, design_url):
    driver = webdriver.Chrome()
    driver.get(design_url)
    wait = WebDriverWait(driver, 10)

    try:
        # Close the pop-up if it appears
        popup_close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "guest-mode-popup__close-button")]')))
        popup_close_button.click()

        # Wait for the text element to be present
        text_element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Name Placeholder"]')))
        text_element.click()

        # Debug: Print the page source to understand the structure
        print(driver.page_source)

        # Wait for the text input to be present and interactable
        text_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))
        text_input.clear()
        text_input.send_keys(name)

        # Wait for the Save button to be clickable
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Save"]')))
        save_button.click()
        time.sleep(5)

        # Wait for the Download button to be clickable
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Download"]')))
        download_button.click()
        time.sleep(5)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        driver.quit()

st.title("Certificate Generator")

uploaded_file = st.file_uploader("Upload a file", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    names = extract_names(image)
    st.write("Extracted Names:")
    for name in names:
        st.write(name)
    
    design_url = st.text_input("Enter Canva design URL")
    if st.button("Generate Certificates"):
        for name in names:
            generate_certificate(name, design_url)
        st.success("Certificates generated successfully!")
