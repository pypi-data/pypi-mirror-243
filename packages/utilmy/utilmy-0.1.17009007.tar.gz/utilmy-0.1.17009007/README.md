
[![Build and Test , Package PyPI](https://github.com/arita37/myutil/actions/workflows/build%20and%20release.yml/badge.svg)](https://github.com/arita37/myutil/actions/workflows/build%20and%20release.yml)

[     https://pypi.org/project/utilmy/#history ](https://pypi.org/project/utilmy/#history)




#### Install
```bash
# conda activate yourENV

git clone https://github.com/arita37/myutil.git
cd myutil
git checkout devtorch

### Install Package in Dev mode
pip install -e .

### How to speed up pandas with cuDF
# References
# Blogpost:         https://developer.nvidia.com/blog/rapids-cudf-accelerates-pandas-nearly-150x-with-zero-code-changes/
# Colab example:    https://nvda.ws/rapids-cudf

# Check GPU
!nvidia-smi

# Install cuDF (this is for cuda11.2-11.8, change it for cuda12)
!pip install cudf-cu11 --extra-index-url=https://pypi.nvidia.com

# Check it works
import cudf 

# Load cuDF
%load_ext cudf.pandas

# That's it.




```









 # Code Foramtter Clang-format
```


### This style was chosen for your .clang-format                                                                                                           
BasedOnStyle: Google                                                                                                                                       
AlignConsecutiveAssignments: true                                                                                                                          
AlignConsecutiveDeclarations: true                                                                                                                         
AlignEscapedNewlines: Right                                                                                                                                
AlignOperands: false                                                                                                                                       
BreakBeforeBinaryOperators: NonAssignment                                                                                                                  
BreakBeforeBraces: Custom                                                                                                                                  
BreakConstructorInitializersBeforeComma: true                                                                                                              
ColumnLimit: 120                                                                                                                                           
Cpp11BracedListStyle: false                                                                                                                                
DerivePointerAlignment: false                                                                                                                              
IndentWidth: 0                                                                                                                                             
MaxEmptyLinesToKeep: 0                                                                                                                                     
PointerAlignment: Middle                                                                                                                                   
SpaceBeforeParens: Always                                                                                                                                  
SpaceBeforeSquareBrackets: true                                                                                                                            
SpaceInEmptyBlock: true                                                                                                                                    
SpaceInEmptyParentheses: true                                                                                                                              
SpacesInSquareBrackets: true                                                                                                                               
                             




```
