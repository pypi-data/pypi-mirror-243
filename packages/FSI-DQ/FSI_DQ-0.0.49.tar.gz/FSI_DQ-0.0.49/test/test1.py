import json
def format_data(input_data):
     
    result={}
    data=input_data
    column_list=data['column_list']
    null_list=data['dq_rules']['Null_check']
    unique_list=data['dq_rules']['Unique_check']
    pattern_list=data['dq_rules']['Pattern_check']
    dtypes=data['classify']['dtypes']
    clasification_list=data['classify']['Classification']

    result['status']='success'
    for key,value in data.items():
        
        
        if key=='business_context':
            for i,j in value.items():
                if i=='entities':
                    bc_dict=j
                    final_list=[]
                    for key, value in j.items():
                        lst={}
                        lst['ColumnName']=key
                        lst['Definition']=value
                        final_list.append(lst)

                    result['business_context_'+i]=final_list
                else:
                    result['business_context_'+i]=j

        

        if key=='dq_rules':
            print('inside dq result')
            count=0
            
            final_list=[]
            final_list_ano=[]
            for l in range (0, len(column_list)):
                lst={}
                lst['Index']=l
                lst['ColumnName']=column_list[l]
                lst['DataType']=dtypes[l]
                lst['IsUnique'] = 1 if column_list[l] in unique_list else 0
                lst['NotNull'] =1 if column_list[l] in null_list else 0
                pattern=""
                if column_list[l] in pattern_list["Columns"]:
                    index = pattern_list["Columns"].index(column_list[l])
                    if index>= len(pattern_list["Patterns"]):
                        pattern=pattern_list["Patterns"][0]
                    else:
                        pattern = pattern_list["Patterns"][index]

                lst['MatchPattern'] =pattern


                lst_ano={}
                lst_ano['Index']=l
                lst_ano['ColumnName']=column_list[l]
                lst_ano['ClassificationLabel']=clasification_list[l]
                
                count=count+1
                final_list.append(lst)
                final_list_ano.append(lst_ano)
            

            result['dq_result']=final_list
            result['anomaly_detection']=final_list_ano

                

            

    formatted_data = json.dumps(result, indent=4)

    return formatted_data



data={"column_list": ["PolicyId", "CustomerId", "PdctId", "PolicyTypeId", "ChannelId", "Duration", "PaymentTypeId", "PremFreq", "PolicyCount", 
"SumAssured", "EffectiveDate", "IssueDate", "CreatedDate", "UpdatedDate"], "business_context": {"name": "Insurance Policy Dataset", "description": "This dataset contains information about insurance policies.", "domain": "Insurance", "entities": {"PolicyId": "Unique identifier for each policy", "CustomerId": "Unique identifier for each customer", "PdctId": "Unique identifier for each product", "PolicyTypeId": "Unique identifier for each policy type", "ChannelId": "Unique identifier for each channel", "Duration": "Duration of the policy in years", "PaymentTypeId": "Unique identifier for each payment type", "PremFreq": "Frequency of premium payments", "PolicyCount": "Number of policies held by the customer", "SumAssured": "Total amount of coverage for the policy", "EffectiveDate": "Date when the policy goes into effect", "IssueDate": "Date when the policy was issued", "CreatedDate": "Date when the policy was created", "UpdatedDate": "Date when the policy was last updated"}}, "dq_rules": {"Null_check": ["PolicyId", "CustomerId", "PdctId", "PolicyTypeId", "ChannelId", "Duration", "PaymentTypeId", "PremFreq", "PolicyCount", "SumAssured", "EffectiveDate", "IssueDate", "CreatedDate", "UpdatedDate"], "Unique_check": ["PolicyId", "CustomerId", "PdctId", "PolicyTypeId", "ChannelId", "Duration", "PaymentTypeId", "PremFreq", "PolicyCount", "SumAssured", "EffectiveDate", "IssueDate", "CreatedDate", "UpdatedDate"], "Pattern_check": {"Columns": ["EffectiveDate", "IssueDate", "CreatedDate", "UpdatedDate"], "Patterns": ["\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}", "\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}", "\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}", "\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}"]}}, "classify": {"Columns": ["PolicyId", "CustomerId", "PdctId", "PolicyTypeId", "ChannelId", "Duration", "PaymentTypeId", "PremFreq", "PolicyCount", "SumAssured", "EffectiveDate", "IssueDate", "CreatedDate", "UpdatedDate"], "Classification": ["numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "numeric", "non-numeric", "non-numeric", "non-numeric", "non-numeric"], "dtypes": ["int", "int", "int", "int", "int", "int", "int", "int", "int", "float", "string", "string", "string", "string"]}}
result=format_data(data)

print(result)