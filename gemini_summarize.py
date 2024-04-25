import json
import glob2
import requests
import google.generativeai as genai 


def summarize_data_with_gemini(data_source, prompt, model="gemini-pro", safety_settings=None):
  """
  This function summarizes data in a CSV file using the Gemini API, 
  incorporating metadata context.

  Args:
      data_source: Path to the CSV file containing the data.
      prompt: Prompt for summarizing the data with context from metadata.
      model: Name of the Gemini model to use (default: "gemini-pro").
      safety_settings: Optional safety settings for the API request.

  Returns:
      A list of summaries, one for each data source-metadata pair.
  """

  summaries = []
  title, texts = [], []

  indicator_files = glob2.glob(f"{data_source}*.csv")
  for each_indicator in indicator_files:

    try:
      with open(each_indicator, "r") as f:
        data_text = f.read()

      print(f"Loaded - {each_indicator}")

      metadata_path = each_indicator.replace(data_source, "metadata/")
      metadata_path = metadata_path.replace('csv', 'json')
      with open(metadata_path, "r") as f:
        metadata = json.load(f)

      print(f"Loaded - {metadata_path}")

    except FileNotFoundError:
      print(f"Error: Data file not found: {each_indicator} - {metadata_path}")
      return summaries

    # Add Gemini API Key
    GOOGLE_API_KEY=None

    if GOOGLE_API_KEY is None:
      print("Warning: Google API key not set. Summaries might not be generated.")
    else:
      
      genai.configure(api_key=GOOGLE_API_KEY)
      model_instance = genai.GenerativeModel(model)
      inputs = [
          prompt,
          f"Raw data:\n{data_text}",
          f"Raw metadata:\n{json.dumps(metadata, indent=4)}"
      ]
      response = model_instance.generate_content(inputs)

      if response:
        print(each_indicator)
        print(metadata)
        os.makedirs('summaries', exist_ok = True)
        data = response.text
        with open(f"summaries/{each_indicator.replace('csv', 'json').replace('data/', '')}", 
                  "w") as f:
          json.dump(data, f, indent=4)

        title.append(metadata[0]['name'])
        texts.append(data)

      else:
        print(f"Error calling Gemini API for {data_source}")
        
  dataset = pd.DataFrame({'title': title, 'text': texts})
  dataset.to_csv('retrieval_data.csv', index=None)


def main():

    prompt = """
    Generate a comprehensive summary based on the provided dataset and metadata. The dataset consists of a single row with multiple columns. Along with this dataset, metadata is provided, detailing the name of the dataset, the source, the methodology of data collection, and any additional descriptive information about what the data represents.

    Use the following guidelines to structure the summary:

    Trend Analysis: Analyze the numerical data to identify trends over the years. Highlight any significant increases, decreases, or anomalies.
    Methodological Context: Incorporate metadata details to enrich the summary. Discuss the data collection methods, source reliability, and the definition of key terms.
    Implications: Discuss the implications.
    Narrative Style: Provide the summary in a clear, narrative style, making it accessible to a broad audience while ensuring it remains informative and data-driven.
    The summary should provide a clear and insightful narrative that not only presents the raw data but also contextualizes it within the broader socio-economic framework of Brazil, leveraging the detailed metadata to enhance understanding and reliability of the information.
    """

    data_source = "data/"
    summarize_data_with_gemini(data_source, prompt)

if __name__=="__main__": 
    main() 