from catalog import CatalogFactory


def main():
    cat = CatalogFactory()
    cat.connect()
    cat.get_workspace('ceshi')
    cat.create_ncstore('nmefc_2016072112_opdr', 'my_test_2', 'nmefc/waterwind')
    pass


if __name__ == '__main__':
    main()
