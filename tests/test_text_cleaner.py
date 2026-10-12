
from src.text_cleaner import clean_text

# Simulate messy text extracted from a resume.
raw_text = "  PYTHON   Developer\n\nwith   Machine Learning skills  "

# Call our function and store the returned result.
cleaned_text = clean_text(raw_text)

# Display the result.
print(cleaned_text)
