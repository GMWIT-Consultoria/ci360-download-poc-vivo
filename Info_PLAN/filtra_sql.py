import json

''' List all output parameters as comma-separated values in the "Output:" docString. Do not specify "None" if there is no output parameter. '''
def execute(datagrid, customer_products):
    'Output:chv_oferta_list, column_offer_list, value_offer_list'

    chv_oferta_list =  []
    column_offer_list =  []
    value_offer_list =  []

    datagrid_json = json.loads(datagrid) # Parse the JSON string into a Python object
    customer_products_list = customer_products.split("; ")
    
    # Extract the metadata and data sections
    metadata = datagrid_json[0]["metadata"]
    data = datagrid_json[1]["data"]
    
    # Extract the column names from the metadata
    column_names = [list(column.keys())[0] for column in metadata]

    # Create a dictionary to store the extracted information
    extracted_data = {column_name: [] for column_name in column_names}
    
    # Iterate over the data rows and extract the values
    for row in data:
        for i, value in enumerate(row):
            column_name = column_names[i]
            extracted_data[column_name].append(value)
    
    # Convert the extracted data dictionary to a list
    extracted_list = [extracted_data[column_name] for column_name in column_names]

    for x in range(len(extracted_list[1])):
        # Checking if the line is of type "Product" and if the products are the same as the customer's
        if ("Products" in extracted_list[1][x]) and (set(customer_products_list) & set((extracted_list[2][x]).split("; "))):
            chv_oferta_list.append(extracted_list[0][x])
            column_offer_list.append(extracted_list[1][x])
            value_offer_list.append(extracted_list[2][x])
    
    return json.dumps(chv_oferta_list), json.dumps(column_offer_list), json.dumps(value_offer_list)