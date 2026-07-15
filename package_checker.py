import requests


def get_package_info(package_name):
    """
    Fetches details about a Python package from the PyPI API
    and returns the parsed JSON data as a Python dictionary.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the internet. Please check your connection.\n")
        return None
    except requests.exceptions.Timeout:
        print("Error: The request took too long and timed out.\n")
        return None

    if response.status_code == 200:
        data = response.json()   # convert JSON text into a Python dictionary
        return data
    elif response.status_code == 404:
        print(f"Error: No package found on PyPI with the name '{package_name}'.\n")
        return None
    else:
        print(f"Error: Something went wrong (status code {response.status_code}).\n")
        return None


def show_package_info(data):
    """Prints selected fields from the parsed JSON package data."""
    info = data.get("info")  # the "info" key holds all the useful details

    print("\n----- PACKAGE INFO -----")
    print("Name       :", info.get("name"))
    print("Version    :", info.get("version"))
    print("Summary    :", info.get("summary"))
    print("Author     :", info.get("author"))
    print("License    :", info.get("license"))
    print("Home Page  :", info.get("home_page"))
    print("-------------------------\n")


def search_keyword_in_summary(data, keyword):
    """
    Simple filtering/search logic: checks whether a given keyword
    appears in the package's summary text.
    """
    info = data.get("info")
    summary = info.get("summary") or ""

    if keyword.lower() in summary.lower():
        print(f"'{keyword}' WAS found in the package summary.\n")
    else:
        print(f"'{keyword}' was NOT found in the package summary.\n")


def compare_versions(data1, data2):
    """
    Compares the latest version numbers of two packages and
    just prints them side by side (simple comparison, no ranking logic).
    """
    info1 = data1.get("info")
    info2 = data2.get("info")

    print("\n----- VERSION COMPARISON -----")
    print(f"{info1.get('name')}: {info1.get('version')}")
    print(f"{info2.get('name')}: {info2.get('version')}")
    print("-------------------------------\n")


def show_menu():
    print("===== PYTHON PACKAGE CHECKER =====")
    print("1. View package info")
    print("2. Search a keyword in a package's summary")
    print("3. Compare two packages")
    print("4. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            package_name = input("Enter package name (e.g. requests): ").strip()
            data = get_package_info(package_name)
            if data is not None:
                show_package_info(data)

        elif choice == "2":
            package_name = input("Enter package name: ").strip()
            data = get_package_info(package_name)
            if data is not None:
                keyword = input("Enter keyword to search: ").strip()
                search_keyword_in_summary(data, keyword)

        elif choice == "3":
            package1 = input("Enter first package name: ").strip()
            package2 = input("Enter second package name: ").strip()
            data1 = get_package_info(package1)
            data2 = get_package_info(package2)
            if data1 is not None and data2 is not None:
                compare_versions(data1, data2)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")


if __name__ == "__main__":
    main()
    

