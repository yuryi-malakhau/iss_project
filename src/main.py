import helper_functions as hf

prompt_message = '''
This program prints and shows location of the International Space Station (ISS)
Available commands:
loc - gives the current geographical location of the ISS
graph - shows the ISS as 0 symbol on the map
pass - prints the passing details of the ISS for your location
people - prints people on the ISS
exit - exits from the program
'''
error_message = 'Something went wrong'


print(prompt_message)
command = ''
if hf.is_internet_on():
    while command != 'exit':
        command = input("Input a command:")
        message = ''
        status = ''
        if command == 'loc':
            status, message = hf.iss_location_string()
            if status:
                print(message)
            else:
                print(error_message)
        elif command == 'pass':
            status, message = hf.iss_overhead_string()
            if status:
                print(message)
            else:
                print(error_message)
        elif command == 'people':
            status, message = hf.iss_people_string()
            if status:
                print(message)
            else:
                print(error_message)
        elif command == 'graph':
            status, message = hf.iss_on_map_string()
            if status:
                print(message)
            else:
                print(error_message)
        elif command == 'exit':
            break
        else:
            print('Wrong command. Try again')
else:
    print('This program requires the Internet connection.')

