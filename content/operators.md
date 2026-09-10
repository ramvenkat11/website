
Each Python operator can be: disallowed or mapped to a user defined function

There are no system defined function - the user has to provide the function that an operator is mapped to. 




The ten operators, by field name: No table is needed. Just the 10 builtin Python operators

The developer sees three options: allow, deny, rewrite. 
When they click rewrite, they are forced to enter a function name
This function must be in the allowlist


The mapped function should maintain the signature/arguments:

* operator should be able to take two numbers. It can't be mapped to a function that takes just a single argument.

Matrix multiplication operator is not checked for the above rule.


There are no "The built-in bounded functions". That's going away. 