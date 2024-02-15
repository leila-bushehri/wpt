from lxml import etree

def validate_xml_and_categorize_commands(xml_file_path, dtd_file_path):
    # Load DTD
    with open(dtd_file_path, 'r') as dtd_file:
        dtd = etree.DTD(dtd_file)
    
    # Load XML
    with open(xml_file_path, 'r') as xml_file:
        xml_root = etree.parse(xml_file)
    
    # Validate XML against the DTD
    is_valid = dtd.validate(xml_root)
    if not is_valid:
        print("XML validation failed.")
        return [], []

    # Initialize variables to hold categorized entries
    led_commands = []
    update_commands = []
    
    # Iterate through each Data in the XML
    for data in xml_root.findall('.//Data'):
        command_element = data.find('.//Command')
        if command_element is not None:
            if command_element.text == 'PUT':
                # LED command logic remains the same
                led_command_details = {
                    "LabelId": data.findtext('.//LabelId'),
                    "Color": data.findtext('.//Color'),
                    "Duration": data.findtext('.//Duration'),
                    "PatternId": data.findtext('.//PatternId')
                }
                led_commands.append(led_command_details)
            elif command_element.text == 'POST':
                # For "POST" commands, treat them as update commands
                update_command_details = {
                    "LabelId": data.findtext('.//LabelId'),
                    "ArtikelNrPSLos": data.findtext('.//ArtikelNrPSLos'),
                    "DMC": data.findtext('.//DMC'),
                    "Kunde": data.findtext('.//Kunde'),
                    "Panel": data.findtext('.//Panel')
                }
                update_commands.append(update_command_details)
    
    return led_commands, update_commands

# Paths to your XML and DTD files
xml_file_path = r"C:\Users\L\Desktop\Wurth\Dummy\wpt_label.xml"
dtd_file_path = r"C:\Users\L\Desktop\Wurth\Dummy\wpt_label_dtd.xml"

led_commands, update_commands = validate_xml_and_categorize_commands(xml_file_path, dtd_file_path)

print(f"LED Commands: {len(led_commands)}")
for cmd in led_commands:
    print(cmd)
print(f"Update Commands: {len(update_commands)}")
for cmd in update_commands:
    print(cmd)
