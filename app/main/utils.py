import zmq
import xml.etree.ElementTree as ET


def send_search_query(query):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")  # Update with your Java backend's address
    xml_data = build_xml_data(query)
    # Send the search query
    socket.send_string(xml_data)

    # Receive the result
    result = socket.recv_string()

    # Clean up resources
    socket.close()
    context.term()

    return result


def build_xml_data(user_input):
    root = ET.Element("query")
    user_input_element = ET.SubElement(root, "userInput")
    user_input_element.text = user_input

    xml_data = ET.tostring(root, encoding="UTF-8", method="xml").decode()
    return xml_data


def client_check():
    port = 5555  # Match the port used by the Java server

    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    # Connect to the server
    socket.connect(f"tcp://127.0.0.1:{port}")

    try:
        while True:
            query = input("Enter a search query (type 'exit' to quit): ")

            if query.lower() == 'exit':
                break
            xml_data = build_xml_data(query)

            # Send the XML data to the server
            socket.send_string(xml_data)

            # Receive the response from the server
            response = socket.recv_string()
            print(f"Server Response: {response}")

    except KeyboardInterrupt:
        pass
    finally:
        socket.close()
        context.term()
