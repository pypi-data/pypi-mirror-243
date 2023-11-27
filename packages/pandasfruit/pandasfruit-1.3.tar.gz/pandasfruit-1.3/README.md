# pandasfruit

Takes in a pandas dataframe and returns a string containing markdown format where the width of the markdown text is more narrow and is suitable for printing. A more narrow table can fit on a printed page, such as a PDF generated from a Jupyter notebook.

Takes in an optional width parameter (number of characters) and will make the resulting markdown this wide. Else will use a default width of 115.

Also will use a default dictionary of words/abbreviations to shorten column names using the abbreviations instead of the original words. Alternatively, a  user-defined dictionary may be passed in.

## Installation
pip install pandasfruit

## Usage
```python
import pandas as pd
from pandasfruit import pandasfruit
```

```python
x = pd.DataFrame(
    {
        'c foobar person number clean': [
            '00000001',
            '00000002',
            '00000003',
            '00000004',
            '00000005',
            '00000006',
            '00000007',
            '00000008'
        ],
        
        'c foobar first name clean': [
            'Eduard',
            'Andriel',
            'Faris',
            'Shaye',
            'Rodney',
            'Arledge',
            'Cory',
            'Madison'
        ],
        
        'c foobar last name clean': [
            'Davis',
            'Bell',
            'Russell',
            'Fisher',
            'Wilson',
            'Campbell',
            'Collins',
            'Thomas'
        ],
        
        'c _foobar_home_street_address_1_clean': [
        
            '1234 Maple Street REALLY REALLY REALLY SUPER REAL LONG '
            'STREET MORE MORE MORE WORDS SOME MORE',
            '5678 Oakwood Avenue',
            '910 Willow Lane',
            '1122 Elm Drive',
            '1314 Cedar Boulevard',
            '1516 Pine Court',
            '1718 Birch Road',
            '1920 Juniper Place REALLY REALLY REALLY SUPER DUPER LONG '
            'APARTMENT NAME EVEN MORE WORDS HERE OK SOME MORE'
        ],

        'c foobar home street address 2 clean': [
            'Apartment 200',
            'Suite 6 MORE MORE MORE AND EVEN MORE WORDS AND ADDING SOME '
            'MORE WORDS AND HERE ARE EVEN SOME MORE AND EVEN MORE WORDS '
            'ARE ADDED HERE OK',
            'Apt. 2',
            'Apartment 4021',
            '2nd Floor',
            'Unit C',
            'Apt. 3',
            'Downstairs'
        ]
    }
)
```
```python
print(x.to_markdown(tablefmt='grid'))
```

+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|    |   c foobar person number clean | c foobar first name clean   | c foobar last name clean   | c _foobar_home_street_address_1_clean                                                                     | c foobar home street address 2 clean                                                                                                    |
+====+================================+=============================+============================+===========================================================================================================+=========================================================================================================================================+
|  0 |                       00000001 | Eduard                      | Davis                      | 1234 Maple Street REALLY REALLY REALLY SUPER REAL LONG STREET MORE MORE MORE WORDS SOME MORE              | Apartment 200                                                                                                                           |
+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|  1 |                       00000002 | Andriel                     | Bell                       | 5678 Oakwood Avenue                                                                                       | Suite 6 MORE MORE MORE AND EVEN MORE WORDS AND ADDING SOME MORE WORDS AND HERE ARE EVEN SOME MORE AND EVEN MORE WORDS ARE ADDED HERE OK |
+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|  2 |                       00000003 | Faris                       | Russell                    | 910 Willow Lane                                                                                           | Apt. 2                                                                                                                                  |
+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|  3 |                       00000004 | Shaye                       | Fisher                     | 1122 Elm Drive                                                                                            | Apartment 4021                                                                                                                          |
+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|  4 |                       00000005 | Rodney                      | Wilson                     | 1314 Cedar Boulevard                                                                                      | 2nd Floor                                                                                                                               |
+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|  5 |                       00000006 | Arledge                     | Campbell                   | 1516 Pine Court                                                                                           | Unit C                                                                                                                                  |
+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|  6 |                       00000007 | Cory                        | Collins                    | 1718 Birch Road                                                                                           | Apt. 3                                                                                                                                  |
+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+
|  7 |                       00000008 | Madison                     | Thomas                     | 1920 Juniper Place REALLY REALLY REALLY SUPER DUPER LONG APARTMENT NAME EVEN MORE WORDS HERE OK SOME MORE | Downstairs                                                                                                                              |
+----+--------------------------------+-----------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------+

```python
x_for_display = pandasfruit.df_to_fitted_markdown(x)

print(x_for_display)
```

+----+------------+----------+-----------+-----------------------------------+-----------------------------------+
|    |      c fbr | c fbr    | c fbr     | c _fbr_home_st_adrs_1_cln         | c fbr home st adrs 2 cln          |
|    |   prsn nbr | first    | last nm   |                                   |                                   |
|    |        cln | nm cln   | cln       |                                   |                                   |
+====+============+==========+===========+===================================+===================================+
|  0 |   00000001 | Eduard   | Davis     | 1234 Maple Street REALLY REALLY   | Apartment 200                     |
|    |            |          |           | REALLY SUPER REAL LONG STREET     |                                   |
|    |            |          |           | MORE MORE MORE WORDS SOME MORE    |                                   |
+----+------------+----------+-----------+-----------------------------------+-----------------------------------+
|  1 |   00000002 | Andriel  | Bell      | 5678 Oakwood Avenue               | Suite 6 MORE MORE MORE AND EVEN   |
|    |            |          |           |                                   | MORE WORDS AND ADDING SOME MORE   |
|    |            |          |           |                                   | WORDS AND HERE ARE EVEN SOME MORE |
|    |            |          |           |                                   | AND EVEN MORE WORDS ARE ADDED     |
|    |            |          |           |                                   | HERE OK                           |
+----+------------+----------+-----------+-----------------------------------+-----------------------------------+
|  2 |   00000003 | Faris    | Russell   | 910 Willow Lane                   | Apt. 2                            |
+----+------------+----------+-----------+-----------------------------------+-----------------------------------+
|  3 |   00000004 | Shaye    | Fisher    | 1122 Elm Drive                    | Apartment 4021                    |
+----+------------+----------+-----------+-----------------------------------+-----------------------------------+
|  4 |   00000005 | Rodney   | Wilson    | 1314 Cedar Boulevard              | 2nd Floor                         |
+----+------------+----------+-----------+-----------------------------------+-----------------------------------+
|  5 |   00000006 | Arledge  | Campbell  | 1516 Pine Court                   | Unit C                            |
+----+------------+----------+-----------+-----------------------------------+-----------------------------------+
|  6 |   00000007 | Cory     | Collins   | 1718 Birch Road                   | Apt. 3                            |
+----+------------+----------+-----------+-----------------------------------+-----------------------------------+
|  7 |   00000008 | Madison  | Thomas    | 1920 Juniper Place REALLY REALLY  | Downstairs                        |
|    |            |          |           | REALLY SUPER DUPER LONG APARTMENT |                                   |
|    |            |          |           | NAME EVEN MORE WORDS HERE OK SOME |                                   |
|    |            |          |           | MORE                              |                                   |
+----+------------+----------+-----------+-----------------------------------+-----------------------------------+