import flask
from flask import request, jsonify
import psycopg2
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def open_pgdb(database="postgres"):
    # connect to database
    pgconn = psycopg2.connect(database=database, user="postgres", password="ratestask", host="127.0.0.1", port="5432")
    # open cursor
    cur = pgconn.cursor()
    return pgconn, cur


def get_children_slugs(cur, port_codes, slug_list):
    '''
    Find all children slugs of the parent slug
    :param cur:        database cursor
    :param port_codes: list, to store all port codes
    :param slug_list:  list, containing parent slugs
    :return:
    '''

    children_slugs = []
    for parent_slug in slug_list:
        # search all children slugs associated with the parent slug
        sql = '''
                SELECT slug FROM regions WHERE parent_slug=%s
                '''
        cur.execute(sql, (parent_slug, ))
        records = cur.fetchall()
        for row in records:
            children_slugs.append(row[0])

        # search all port codes belonging to this parent slug
        sql2 = '''
                SELECT code FROM ports WHERE parent_slug=%s
                '''
        cur.execute(sql2, (parent_slug, ))
        records2 = cur.fetchall()  # one slug may have several ports
        for row in records2:
            port_codes.append(row[0])

    return children_slugs


def get_port_code(cur, slug):
    '''
    Find all port codes associated with the input slug
    :param cur:  database cursor
    :param slug: string, URL's input, destination (or origin)
    :return:
    '''

    port_codes = []  # store all port codes

    children_slugs = get_children_slugs(cur, port_codes, [slug])

    # if slug == 'northern_europe', then it has many child regions
    # and need to continue finding out the port codes belonging to child regions
    while len(children_slugs) > 0:
        children_slugs = get_children_slugs(cur, port_codes, children_slugs)

    return port_codes


@app.route('/rates', methods=['GET'])
def api_filter():
    query_parameters = request.args

    date_from = query_parameters.get('date_from').strip()
    date_to = query_parameters.get('date_to').strip()
    # assume "origin" and "destination" are obtained from database and
    # hence they do not contain special characters(e.g., >, <, !) and other errors
    origin = query_parameters.get('origin').strip()
    destination = query_parameters.get('destination').strip()

    # connect to database
    pgconn, cur = open_pgdb()

    orig_port_codes = []
    dest_port_codes = []

    # not sure whether the origin is always an individual 5-character port code ???
    if origin.isupper() and len(origin) == 5:
        orig_port_codes.append(origin)
    else:
        orig_port_codes = get_port_code(cur, origin)


    if destination.isupper() and len(destination) == 5:
        dest_port_codes.append(destination)
    else:
        # if the input is a parent slug(e.g., scandinavia) rather than a 5-character port code,
        # then it has multiple ports
        dest_port_codes = get_port_code(cur, destination)


    results = []
    for orig_code in orig_port_codes:

        day_prices = {}
        for dest_code in dest_port_codes:

            sql = '''
                    SELECT price, day FROM prices WHERE
                    day >= TO_DATE(%s,'YYYY-MM-DD') AND day <= TO_DATE(%s, 'YYYY-MM-DD')
                    AND orig_code=%s AND dest_code=%s
                    '''

            cur.execute(sql, (date_from, date_to, orig_code, dest_code))
            records = cur.fetchall()
            for row in records:
                if row[1] not in day_prices:
                    day_prices[row[1]] = [row[0]]
                else:
                    day_prices[row[1]].append(row[0])


        for day_key in day_prices:
            item_info = {}
            if len(day_prices[day_key]) < 3:  # less than 3 prices for this route, return null
                item_info['average_price'] = None
            else:
                all_prices = day_prices[day_key]
                avg_price = round(sum(all_prices) / len(all_prices), 2)
                item_info['average_price'] = avg_price

            # format datetime, YYYY-MM-DD
            item_info['day'] = day_key.strftime('%Y-%m-%d')
            results.append(item_info)

    # disconnect the database
    pgconn.close()

    # sort final results by day
    results.sort(key=lambda x: x['day'])

    return jsonify(results)


app.run(host='0.0.0.0', port=5002)


