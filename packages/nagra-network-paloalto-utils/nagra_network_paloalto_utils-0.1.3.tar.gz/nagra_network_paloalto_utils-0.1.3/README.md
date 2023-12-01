# Utils

Palo Alto script repository


## Concerned repositories
Nb: We must not manage here other repositories referencing these utils. The list maitained here is **TEMPORARY** and will only be used to compensiate the lack of documentation.

(updated on 24.11.2023)
* https://gitlab.kudelski.com/network/paloalto/corporate/security-policies/-/blob/master/.gitlab-ci.yml?ref_type=heads
    * "checks.py" => yaml check
    * tags (creation or check ?)
    * addresses (creation or check ?)
    * services (creation or check ?)
    * application (creation or check ?)
    * indexes
    * git_writer

* https://gitlab.kudelski.com/network/paloalto/corporate/nat/-/blob/main/.gitlab-ci.yml?ref_type=heads
    * yaml check on data/
* https://gitlab.kudelski.com/network/paloalto/rar/-/blob/master/.gitlab-ci.yml?ref_type=heads
    * Indexes check on 2 security rules files

* https://gitlab.kudelski.com/network/paloalto/global/objects/-/blob/master/.gitlab-ci.yml?ref_type=heads
    * Check yaml files (addresses, services, tags)
    * Check if we can delete objects
