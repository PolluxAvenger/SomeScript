# coding=utf-8

import shodan


def shodanSearch(keywords, key):
    host_list = []
    total_number = 0
    Shodan_API_key = key

    try:
        api = shodan.Shodan(Shodan_API_key)
        results = api.search(keywords)
        total_number = int(results['total'])
		
        for result in results['matches']:
            host_list.append({"domain":result['domains'], "ip":result['ip_str'], "port":result['port'],
                              "country":result['location']['country_name'], "timestamp" : result['timestamp']})
		
        return total_number, host_list

    except shodan.APIError as e:
        print(str(e))


if __name__ == '__main__':
    total_number, host_list  = shodanSearch('wordpress', 'your_api_key')
    print('------------------------------------------')
    print(total_number)
    print('------------------------------------------')
    print(len(host_list))
    print('------------------------------------------')
    print(host_list)
