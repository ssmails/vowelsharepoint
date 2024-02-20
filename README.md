
#### Vowel Sharepoint 
Interfaces with Sharepoint APIs, SDKs. 

#### Usage
pip install git+https://wwwin-github.cisco.com/vowel-it/vowelsharepoint.git

#### References

This package currently heavily uses the following lib for Sharepoint access.
https://github.com/vgrem/Office365-REST-Python-Client

#### Known Issues with this Library:

- Slow downloads
```
https://github.com/vgrem/Office365-REST-Python-Client/issues/790
```

- Errored downloads without warnings
```
https://github.com/vgrem/Office365-REST-Python-Client/issues/782
https://github.com/vgrem/Office365-REST-Python-Client/issues/776
```

- Possible open issues reading large folders
SharePoint list view threshold = 5,000 items
```
https://github.com/vgrem/Office365-REST-Python-Client/issues/636
https://github.com/vgrem/Office365-REST-Python-Client/issues/558
https://github.com/vgrem/Office365-REST-Python-Client/issues/392
https://github.com/vgrem/Office365-REST-Python-Client/issues/637
```
