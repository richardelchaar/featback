import openai
import json


def extract_features_with_llm(post_title, post_text, product):
    """Use LLM to extract product features and emotions from post text."""
    prompt = f"""
    Here is a Reddit post regarding the following product: {product}
    
    Title : "{post_title}"
    
    Post: "{post_text}"
    
    If this is feedback, a review, or an opinion about the product:
    1. Identify the product feature or aspect being discussed and classify the feature into one of these categories for each of the features: 
       - Battery (General, Battery duration, Charging speed, Battery health, Wireless charging)
       - Camera (General, Photo quality, Video recording, Camera features, Zoom capability, Flash)
       - Display (General, Screen resolution, Refresh rate, Brightness levels, Screen durability)
       - Performance (General, Processor speed, Gaming performance, Multitasking, Software lag)
       - Connectivity (General, 5G compatibility, Wi-Fi issues, Bluetooth stability, Dual SIM support)
       - Design (General, Material, Weight, Color options, Water resistance)
       - Software (General, Update frequency, Pre-installed apps, Customization, Privacy settings)
    2. Identify the user’s emotion or sentiment (e.g., "Excitement", "Satisfaction", "Joy", "Relief", "Trust", 
         "Disappointment", "Frustration", "Anger", "Confusion", "Regret", 
         "Curiosity", "Surprise", "Skepticism", "Indifference", "Anticipation").
    3. Provide a **reason** from this list:
        "Below Expectations", "Above Expectations", "Functionality", "Reliability", "Ease of use", 
         "Accessibility", "Design", "Build quality", "Overheating", "Compatibility"


    5. Respond with the following format:
    [
      {{"type": "review", "category": "Battery life", "feature": "Battery duration", "emotion": "Disappointment", "reason": "Below Expectations"}},
      {{"type": "review", "category": "Camera", "feature": "Camera features", "emotion": "Excitement", "reason": "Ease of use"}}
    ]


    If this is a question or inquiry about the product:
    
    1. Identify the product feature or aspect being inquired about.
    2. Classify the feature into one of the categories shown above.
    2. Classify the question into one of these categories: 
       - "General question", "How-to-use inquiry", "Recommendation request", 
         "Product comparison inquiry", "Feature inquiry".
    3. respond with the following format:
    [
      {{"type": "question", "category": "Battery life", "feature": "Battery duration", "reason":"Product comparison inquiry"}}
    ]

    If the post is irrelevant or not related to the product, return: []
    
    Do not respond with any other text
    """

    try:

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts structured insights from Reddit posts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
    except Exception as e:

        raise RuntimeError(f"Unexpected error during OpenAI API call: {e}")


    response_text = response.choices[0].message.content.strip()
    response_json = json.loads(response_text)


    return response_json
