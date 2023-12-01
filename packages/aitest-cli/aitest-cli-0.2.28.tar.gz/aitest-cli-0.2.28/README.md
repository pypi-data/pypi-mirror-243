# aitest
The  aitest  Command  Line  Interface is a unified tool to manage your aitest services.

### Installing
To install this CLI tool you can run the below command for Linux 
```
pip3 install aitest-cli
```

To install this CLI tool you can run the below command for windows 
```
pip install aitest-cli
```

### How to get configuration information
    1) To get User Identifier follow below steps:

        visit aitest -> settings -> copy User Identifier.

    2) To get the Client ID and Client secret ID  you need to send a request via email to this email id aitest-support@appliedaiconsulting.com . You will receive the Client ID and Client secret ID via email.


### How to use
    To see help text, you can run:

    aitest --help
    aitest <command> --help
    aitest <command> <subcommand> --help

    ex:
    1) If you want help to understand aitest CLI, you can run the following command:
    Input :
    
        aitest --help
        
    output:
    
        Usage: aitest [OPTIONS] COMMAND [ARGS]...

        The  aitest  Command  Line  Interface is a unified tool to manage your aitest  services.
    
        To see help text, you can run:
    
       aitest --help
    
       aitest <command> --help
    
       aitest <command> <subcommand> --help
    
       Options:
           --help  Show this message and exit.
    
       Commands:
           configure  If this command is run with no arguments, you will be prompted...
           run        If this command is run with testrun id as an argument, aitest...
           status     If this command is run with testrun id as an argument, aitest...

    2) If you want to know how configure command works , you can run the following command:
        Input:
        
            aitest configure --help
        
        Output:
        
        aitest configure [OPTIONS]

        If this command is run with no arguments, you will be prompted for configuration values such as your  aitest  User ID, Client ID and Client Secret ID.If your configure file
        does not  exist (the default location is ~/.aitest/configure), the aitest
        CLI will create it for you.To keep an existing value, hit enter when
        prompted for the value.

    
        To save the configurations , you can run below command:
    
        aitest configure
    
       Options:
          --help  Show this message and exit.
          --env  This options is to set the AITEST Environment by deafult it is set to PROD.


    3) How to run aitest configure command?
        Input:

                aitest configure [-e optional]

        Output:
    
                Enter aiTest User Identifier : 
                Enter Client ID :
                Enter Client Secret ID :
        
#### Note : To access the aitest services using CLI commands you need to run  aitest configure command first.


    4) How to run aitest run command?:
        Input:
        
            aitest run -id 69cd8eb8-9700-11ed-bdc9-3e71e7127aff -p test-password -w 5       

        Output:
        
        Test created successfully
        Test Name : Test 1
        Testrun ID : 47782fb0-9711-11ed-809d-62cd909dddc7

        Testrun is in progress, result will be displayed once it get completed.

        test status : completed

        +--------------+-----------------+--------------------------------------+--------+------------+
        | browser_name | browser_version |          test run result id          | status | time taken |
        +--------------+-----------------+--------------------------------------+--------+------------+
        |   firefox    |       104       | 47c53f08-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.001    |
        |   firefox    |       104       | 47d350e8-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.001    |
        |   firefox    |       104       | 47deb2b2-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.001    |
        |   firefox    |       104       | 47eca5fc-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.001    |
        |   firefox    |       104       | 47fa16ec-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.002    |
        +--------------+-----------------+--------------------------------------+--------+------------+

    Note : Enter git password only if you used git url for creating the test otherwise no need to enter git password
            
    5) How to run aitest status command?
        Input :

            aitest status -id 47782fb0-9711-11ed-809d-62cd909dddc7

        Output:

            test status : completed

            +--------------+-----------------+--------------------------------------+--------+------------+
            | browser_name | browser_version |          test run result id          | status | time taken |
            +--------------+-----------------+--------------------------------------+--------+------------+
            |   firefox    |       104       | 47c53f08-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.001    |
            |   firefox    |       104       | 47d350e8-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.001    |
            |   firefox    |       104       | 47deb2b2-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.001    |
            |   firefox    |       104       | 47eca5fc-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.001    |
            |   firefox    |       104       | 47fa16ec-9711-11ed-b277-c6d8e5da78fe |  fail  |   0.002    |
            +--------------+-----------------+--------------------------------------+--------+------------+




    

    

    