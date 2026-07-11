import json
import subprocess


def generate_srs_domains(domains: list[str], domain_regexes: list[str]):
    rules = []
    if domains:
        rules.append({"domain_suffix": domains})
    if domain_regexes:
        rules.append({"domain_regex": domain_regexes})

    data = {
        "version": 3,
        "rules": rules,
    }
    srs_file_path = "domains.srs"
    json_file_path = "domains.json"
    try:
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

        subprocess.run(
            ["sing-box", "rule-set", "compile", json_file_path, "-o", srs_file_path],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"Compile error {json_file_path}: {error}")
    except Exception as error:
        print(f"Error while processing {domains}: {error}")


def main():
    domains = []
    domain_regexes = []
    with open("domains.lst") as domain_list:
        for line in domain_list:
            domain = line.strip()
            if domain and domain[0] not in ["/", "#"]:
                if domain.startswith("^") and domain.endswith("$"):
                    domain_regexes.append(domain)
                else:
                    domains.append(domain)

    generate_srs_domains(domains, domain_regexes)


if __name__ == "__main__":
    main()
