path = input('? Enter path to inference.atp (this can later be changed in the .env file): ')
with open('.env', 'w') as f : 
    f.write(f'PATH_TO_INFERENCE={path}\n') 
