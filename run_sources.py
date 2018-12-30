"""
Run all sources to collect domain from registered sources.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""

import sources


def main():
    """Main method for running all sources."""
    for source in sources.__all__:
        print(source.get_cycle())


if __name__ == "__main__":
    main()
