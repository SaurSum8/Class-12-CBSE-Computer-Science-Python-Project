# Class-12-CBSE-Computer-Science-Python-Project
My Computer Science Project For CBSE Class 12 (2023-2024) - A Game Store Kiosk/DBMS Using Python &amp; MySQL library

The following was directly copied and pasted from my 'Flow Of Project' section of my report :P -

When the kiosk is started, the connection to SQL
and database is handled, alongside checks of required
tables (Inventory and Membership Tables). If anything
is missing, the program automatically creates the
required tables or database. Then `greet()` is called to
greet customers, then `menu()` function is called.
From here, our project can ‘flow in three ways’ based
on the input -

- Flow For Purchaser:
1. Option 1 is selected and all products for sale are
displayed alongside their ID and information
regarding their category, age requirement, release
date, price and available stock. [`purchaser()` called]
2. Users can input -1 to return to the menu and -2 to
search products by category.
3. To purchase an item, the user enters the ID of the
product, then enters their year of birth (to ensure
they meet minimum age requirements).
[`ageCheck(ID)` called]
4. If they are old enough, they can proceed and enter
the quantity of purchase (if they aren’t old enough
it returns to the purchase menu).
5. After confirming, they can enter their membership
ID to use/get points for this purchase. If they are
not a member, they can skip to checkout or register
themselves. [`memCheck()` called]
6. They can confirm the purchase now, if it were
successful, the database for stock and membership
points (if they were a member) is updated. Else, if
it were unsuccessful, the database is not updated.
[`checkout(ID, Quan)` called]
7. The program returns back to the main menu after
this.
- NOTE: This system is designed to be very
user-friendly, if the customer were to make an
incorrect / error causing input at any time, the
program is designed to handle this and alert the
user. This is achieved using try/except statements
and our `inputChoiceHandler(x,y,z)` function.

- Flow For Membership Checking:
1. Option 2 is selected or we are at membership
checking part of the purchasing section.
[`memCheck()` called]
2. If they already are a member, they are asked to
enter their unique ID, and can then see their
membership points. If they are purchasing
something, they can enter the number of points to
use for said purchase.
3. If they are not a member, they are asked if they
want to register for membership. If not, they are
returned to the menu or proceeded to the checkout
section.
4. If yes, they are asked for their name and phone
number. A random, unique membership ID is
generated under their name. They are now
registered with the membership program.
[`memRegister()` called]
5. They return to the membership menu and continue
from stage 2, as mentioned above.
Note: 15% of the amount they pay in a given purchase
is added to their membership account. 1 point = 1 unit
of currency here.

- Flow For Admin:
1. Option 3 is selected and the admin password is
asked (to ensure the safety of the store database). If
the correct password is given, the user has access
to the admin panel; else, the program returns back
to the main menu. [`adminPanel()` called]
2. There are 12 total choices.
3. Choice 1 prints the contents of the ‘Inventory’
table. [`tablePrint(1)` called]
4. Choice 2 prints the contents of the ‘Membership’
table. [`tablePrint(0)` called]
5. Choices 3 and 4 reset ‘Inventory’ and
‘Membership’ tables respectively. [`‘TRUNCATE’`
SQL command executed]
6. Choices 5 and 6 can be used to insert into/delete
from the ‘Inventory’ table. [`insert(1)` or `delete(1)`
called respectively]
7. Choices 7 and 8 can be used to insert into/delete
from the Membership’ table. [`insert(0`) or
`delete(0)` called respectively]
8. Choices 9 and 10 allow admin to update any field
of a selected record from ‘Inventory’ or
‘Membership’ respectively (record is selected
using record’s current ID). [`update(0)` or
`update(1)` called respectively]
9. Choice 11 can be used to shut down the kiosk
system. [Using `sys.exit()`]
10. Choice 12 returns the program back to the main
menu.
