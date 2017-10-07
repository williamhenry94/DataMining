import pip
import os
installed_packages = pip.get_installed_distributions()
flat_installed_packages = [package.project_name for package in installed_packages]
# print (flat_installed_packages)

must_have = ['matplotlib','scikit-learn', 'pandas','numpy']

must_have_set = set(must_have)
flat_installed_packages_set = set(flat_installed_packages)

diff = must_have_set - flat_installed_packages_set

if len(diff) == 0:
    print ("Every this is already installed")
    
else:
    for i in must_have:
        if i not in flat_installed_packages:
            try:
                os.system("pip install "+i)
            except Exception as e:
                print (e)
    

