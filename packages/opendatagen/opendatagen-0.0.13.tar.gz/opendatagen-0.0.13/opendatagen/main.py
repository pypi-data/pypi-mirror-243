from opendatagen.template import Template, TemplateManager, TemplateName, Variable
from opendatagen.data_generator import DataGenerator
from opendatagen.model import OpenAIChatModel, OpenAIInstructModel, OpenAIEmbeddingModel, ModelName
from opendatagen.anonymizer import Anonymizer
from opendatagen.utils import function_to_call
from opendatagen.agent import DataAgent
import warnings
import json 
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def anonymize_text(): 

    text_to_anonymize = """
            My name is Thomas, Call me at 0601010129 or email me at john.doe@example.com. 
            My SSN is 123-45-6789 and 4242 4242 8605 2607 is my credit card number. 
            Living in the best city in the world: Melbourne.
            New York & Co is a restaurant.
            It is 10 am.
            I have 10€ in my pocket. Oh my god.
            I have park my Tesla next to your house.
            My id is 0//1//2//2//2//2
    """
    
    completion_model = OpenAIChatModel(model_name="gpt-4-1106-preview")

    anonymizer = Anonymizer(completion_model=completion_model)

    anonymized_text = anonymizer.anonymize(text=text_to_anonymize)
    
    print(anonymized_text)

def generate_data_from_predefined_template(): 

    manager = TemplateManager(template_file_path="template.json")
    template = manager.get_template(template_name="chunk3")

    if template:
        
        generator = DataGenerator(template=template)
        
        data = generator.generate_data(output_path="output_nyt.csv")
        
        print(data)
    
def generate_data_from_user_defined_template():    

    # Create the custom template using the Pydantic models
    user_template = Template(
        description="Custom template for Python exercises",
        prompt="Python exercice statement: {python_exercice_statement}",
        completion="Answer:\n{python_code}",
        prompt_variation_number=1,
        prompt_variables={
            "python_exercice_statement": Variable(
                name="Python exercice statement",
                temperature=1,
                max_tokens=120,
                generation_number=10
            )
        },
        completion_variables={
            "python_code": Variable(
                name="Python code",
                temperature=0,
                max_tokens=256,
                generation_number=1
            )
        }
    )

    generator = DataGenerator(template=user_template)
    
    data = generator.generate_data(output_path="output.csv")

    print(data)


def generate_variation_from_variable():

    manager = TemplateManager(template_file_path="template.json")
    template = manager.get_template(TemplateName.PRODUCT_REVIEW)

    generator = DataGenerator(template=template)

    prompt = template.prompt 
    #prompt = Write a review of '{product_name}' made by {brand}:
    prompt_variables = generator.extract_variable_from_string(prompt) 

    prompts_parameters = generator.contextual_prompt_generation(prompt=prompt, 
                                                                variables=prompt_variables, 
                                                                current_variation_dict={}, 
                                                                fixed_variables=template.prompt_variables)
    
    print(prompts_parameters)



def validate_chunk(result: dict):
    # Define the schema
    schema = {
        "type": "object",
        "properties": {
            "chunks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "first_words": {"type": "string"},
                        "last_words": {"type": "string"}
                    },
                    "required": ["first_words", "last_words"]
                }
            }
        },
        "required": ["chunks"]
    }

    json_string = result["generated_value"]
    article_content = result["article_content"].lower()

    try:
        # Parse the JSON string
        json_data = json.loads(json_string)
        
        # Validate the JSON data against the schema
        validate(instance=json_data, schema=schema)

        # Check if each start and end value is in the article content
        errors = []
        for i, chunk in enumerate(json_data["chunks"], start=1):
            first_words, last_words = chunk["first_words"].lower(), chunk["last_words"].lower()
            if first_words not in article_content:
                errors.append(f"Chunk {i} first_words not found: '{first_words}' in article_content")
            if last_words not in article_content:
                errors.append(f"Chunk {i} last_words not found: '{last_words}' in article_content")

        if errors:
            return False, "Errors found in chunks: " + "; ".join(errors)
        
        return True, "The JSON complies with the schema and all chunks are correctly found in the article content."

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {e}"

    except ValidationError as e:
        return False, f"The JSON does not comply with the schema: {e}"

if __name__ == "__main__":

    #agent = DataAgent()
    #agent.run()

    #anonymize_text()
    generate_data_from_predefined_template()

    #generate_data_from_user_defined_template()

    #generate_variation_from_variable()
    