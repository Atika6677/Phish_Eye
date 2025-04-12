from transformers import pipeline

URL_Classification = pipeline("text-classification", model="imanoop7/bert-phishing-detector")
  
def URL_Classifier(url):
    """s
    Classifies the given URL as phishing or benign.

    Parameters:
    url (str): The URL to be classified.

    Returns:
    int: 1 if the URL is classified as phishing, 0 if benign.
    """
    print("\nEntering URL Classification...")

    try:
        prediction = URL_Classification(url, truncation=True, max_length=512)

        label = prediction[0]['label']

        if label == "Not Safe":
            print("URL is classified as phishing!")
            return 1
        
        else:
            print("URL is classified as benign...")
            return 0

    except Exception as e:

        print(f"Error processing URL Classifier: {e}")
        return 0