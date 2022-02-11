# -*- coding: utf-8 -*-
from yzspider.spider import save_excel, transfer, yz_school_info_spider, yz_school_url_spider, yz_major_spider


def main():
    save_excel(transfer(yz_school_info_spider(yz_school_url_spider(yz_major_spider()))))


if __name__ == '__main__':
    main()
