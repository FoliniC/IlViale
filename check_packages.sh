#!/bin/bash

# List of packages to check
packages=(
    "asgiref==3.8.1"
    "astroid==3.3.8"
    "atomicwrites==1.3.0"
    "attrs==19.3.0"
    "beautifulsoup4==4.12.3"
    "boto3==1.16.54"
    "botocore==1.19.54"
    "bsdiff4==1.2.0"
    "colorama==0.4.3"
    "concurrent-log-handler==0.9.19"
    "dill==0.3.9"
    "django==4.2.18"
    "django-braces==1.13.0"
    "django-classy-tags==4.1.0"
    "django-environ==0.4.5"
    "django-newsletter==1.0"
    "django-sitetree==1.18.0"
    "factory-boy==2.12.0"
    "faker==4.0.1"
    "feedparser==6.0.11"
    "feedreader==0.3.1"
    "future==0.18.3"
    "iniconfig==2.0.0"
    "isort==4.3.21"
    "jmespath==0.10.0"
    "lazy-object-proxy==1.4.3"
    "ldif3==3.1.1"
    "lxml==5.3.0"
    "mccabe==0.6.1"
    "more-itertools==8.2.0"
    "packaging==20.3"
    "platformdirs==4.3.6"
    "pluggy==0.13.1"
    "portalocker==2.0.0"
    "protobuf==3.18.3"
    "py==1.10.0"
    "pylint==3.3.3"
    "pyparsing==2.4.6"
    "pyrfc3339==1.1"
    "pytest==7.2.0"
    "pytest-runner==5.2"
    "python-card-me==0.9.3"
    "python-dateutil==2.8.1"
    "pytz==2019.3"
    "requests-mock==1.7.0"
    "s3transfer==0.3.4"
    "sgmllib3k==1.0.0"
    "six==1.14.0"
    "sorl-thumbnail==12.7.0"
    "sorl-watermark==1.0.0"
    "soupsieve==2.0"
    "sqlparse==0.5.0"
    "surlex==0.2.0"
    "text-unidecode==1.3"
    "tomlkit==0.13.2"
    "ua-parser==0.10.0"
    "unicodecsv==0.14.1"
    "user-agents==2.2.0"
    "wcwidth==0.1.8"
    "wrapt==1.11.2"
    "django-tinymce"
    "pyyaml"
    "ua-parser"
    "user-agents"
    "django-user-agents"
    "django_ses"
    "django-cookie-law"
    "django-admin"
    "redis"
)

# Function to check if a package is installed using dpkg or pip
check_package() {
    package_name=$(echo $1 | cut -d'=' -f1)
    
    if dpkg -l | grep -iq "^ii  $package_name"; then
        echo "$package_name: Installed via dpkg"
    elif pip show $package_name &> /dev/null; then
        echo "$package_name: Installed via pip"
    else
        echo "$package_name: Not Installed"
    fi
}

# Loop through the list of packages and check each one
for pkg in "${packages[@]}"; do
    check_package "$pkg"
done
