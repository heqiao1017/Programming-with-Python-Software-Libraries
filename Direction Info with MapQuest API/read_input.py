#A module that reads the input and constructs the objects that
#will generate the program's output.
#This is the only module that should have an
#if __name__ == '__main__' block to make it executable;
#you would execute this module to run your program.
import interact_API
import output

SUCCESS_ROUTE=0
NO_ROUTE_FOUND=1
MAPQUEST_ERROR=2

def read_input()->[]:
    number=input()
    input_list=[]
    for x in range(int(number)):
        input_item=input()
        input_list.append(input_item)
    return input_list

def construct_output_object_list(output_list:[])->[]:
    output_object_list=[]
    for item in output_list:
        if item=='LATLONG':
            output_object_list.append(output.LatLng())
        if item=='STEPS':
            output_object_list.append(output.Directions())
        if item=='TOTALTIME':
            output_object_list.append(output.TotalTime())
        if item=='TOTALDISTANCE':
            output_object_list.append(output.Distance())
        if item=='ELEVATION':
            output_object_list.append(output.Elevation())
    return output_object_list

def check_error(search_result_dict:dict)->SUCCESS_ROUTE or NO_ROUTE_FOUND or MAPQUEST_ERROR:
    code = search_result_dict['info']['statuscode']
    if code==0:
        return SUCCESS_ROUTE
    elif code==400:
        return NO_ROUTE_FOUND
    else:
        return MAPQUEST_ERROR

def display_output_list(output_object_list:[], search_result_dict:dict):
    for item in output_object_list:
        print()
        if type(item)==output.Elevation:
            print('ELEVATIONS')
            display_elevation(search_result_dict,item)
        else:
            item.display_output(search_result_dict)
            
def display_elevation(search_result_dict:dict, output_item):
    #search for elavation one by one
    lat_lng_collection=output.get_lat_lng_collection(search_result_dict)
    elevation_url_list=interact_API.build_elevation_urls(lat_lng_collection)
    for url in elevation_url_list:
        search_result_dict=interact_API.get_json_result(url)
        output_item.display_output(search_result_dict)
    
def print_copyright_statement():
    print('\nDirections Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors.')

def show_output(statuscode: int, search_result_dict:dict, output_object_list:[]):
    if statuscode==SUCCESS_ROUTE:
        display_output_list(output_object_list,search_result_dict)
    elif statuscode==NO_ROUTE_FOUND:
        print('\nNO ROUTE FOUND')
    else:
        print('\nMAPQUEST ERROR')

def user_interface()->None:
    #get the user input
    location_list=read_input()
    output_list=read_input()
    #process the input
    #get the direction url and json search result dictionary by using the location list
    direction_url=interact_API.build_direction_url(location_list)
    search_result_dict=interact_API.get_json_result(direction_url)
    #check and print the output list by constructing different output objects
    output_object_list=construct_output_object_list(output_list)
    status_code=check_error(search_result_dict)#check if there is any error before display the ouput
    show_output(status_code,search_result_dict,output_object_list)#show output or error messages
    print_copyright_statement()

if __name__=='__main__':
    user_interface()
    
