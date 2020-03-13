from catalog import CatalogFactory


def main():
    cat = CatalogFactory()
    cat.connect()
    # TODO:[*] 20-03-13 此处存在一个问题
    cat.get_workspace('ceshi')
    cat.create_ncstore('nmefc_2016072112_opdr', 'my_test_2', 'nmefc/waterwind')
    cat.create_coverage('my_test_2', 'ceshi_coverage_01', 'nmefc_2016072112_opdr')
    pass


if __name__ == '__main__':
    main()
