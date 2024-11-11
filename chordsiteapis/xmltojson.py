import os
import xml.etree.ElementTree as ET
import json

# Change to the specified directory
os.chdir(r'D:\headerdesigns')

def xml_to_json(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    annotations = []
    
    # Extract the filename from the XML
    filename = root.find('filename').text
    print("Found image file:", filename)  # Debug: print found image filename

    # Create a dictionary to store image data
    image_data = {
        'filename': filename,
        'annotations': []
    }
    
    # Iterate over each object in the XML
    for obj in root.findall('object'):
        label = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)
        
        print("Found object:", label)  # Debug: print found object labels

        annotation = {
            'label': label,
            'coordinates': {
                'x': xmin,
                'y': ymin,
                'width': xmax - xmin,
                'height': ymax - ymin
            }
        }
        image_data['annotations'].append(annotation)
    
    # Append the image data to annotations list
    annotations.append(image_data)

    return json.dumps(annotations, indent=4)

# Print the current working directory for debugging
print("Current Working Directory:", os.getcwd())

# Usage: Iterate over all XML files in the directory
try:
    for xml_filename in os.listdir(os.getcwd()):
        if xml_filename.endswith('.xml'):  # Check for XML files
            json_data = xml_to_json(xml_filename)  
            if json_data:
                # Create a JSON filename based on the XML filename
                json_filename = xml_filename.replace('.xml', '.json')
                with open(json_filename, 'w') as json_file:
                    json_file.write(json_data)
                print(f"Conversion successful. JSON saved as '{json_filename}'.")
            else:
                print(f"No data found to convert for {xml_filename}.")
except FileNotFoundError as e:
    print(e)
