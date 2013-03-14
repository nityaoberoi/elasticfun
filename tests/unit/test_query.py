import sure
from datetime import datetime
from elasticfun import Query, ParsingException


def test_query_all():
    # When I query for all the objects
    querystr = str(Query())

    # Then I see that the right query was created
    querystr.should.equal('*:*')


def test_empty_query():
    # When I query for nothing
    querystr = str(Query.empty())

    # Then I see that this query object won't return anything just yet
    querystr.should.be.empty


def test_mixing_words_and_fields():
    # When I try to filter by both words and fields in the same object,
    # Than I see that it actually raised an exception
    Query.when.called_with('stuff', field='val').should.throw(
        ParsingException,
        "You cannot use both words and fields in the same call. "
        "You should do something like this: qb('stuff') & qb(field='val')")


def test_passing_more_than_one_field():
    # When I try to filter with more than one field in the same object,
    # Than I see that it actually raised an exception
    Query.when.called_with(field1='a', field2='b').should.throw(
        ParsingException,
        "You cannot use more than one field the same call. "
        "You should do something like this: qb(field2='b') & qb(field1='a')")


def test_query_single_word():
    # When I filter by a certain word.
    query = Query('stuff')

    # Then I see that the right query was created
    str(query).should.equal('"stuff"')


def test_query_single_field():
    # When I filter by a certain field.
    query = Query(brand='blah')

    # Then I see that the right query was created
    str(query).should.equal('brand:"blah"')


def test_query_single_boolean_value():
    # When I filter by a boolean value
    query = Query(True)

    # Then I see that the right query was created
    str(query).should.equal('"True"')


def test_query_single_datetime_value():
    # When I filter by a boolean value.
    query = Query(datetime(2013, 3, 13, 1, 32))

    # Then I see that the right query was created with the date
    # converted to a string in the YYYY-mm-ddTHH:MM:SS format
    str(query).should.equal('"2013-03-13T01:32:00"')


def test_query_with_and():
    # When I filter by one word after another
    query = Query('ice') & Query('cream')

    # Then I see that the right query was created with the AND operator
    str(query).should.equal('("ice" AND "cream")')


def test_query_with_or():
    # When I filter by one word and then by another word with the OR
    # operator
    query = Query('ice') | Query('cream')

    # Then I see that the right query was created
    str(query).should.equal('("ice" OR "cream")')


def test_query_with_two_words():
    # When I filter by two words in the same filter
    query = Query('ice cream')

    # Then I see that the right query was created with an AND separating
    # the two words
    str(query).should.equal('"ice cream"')


def test_query_with_field_and():
    # When I filter by field with more than one value
    query = Query(brand='ice cream')

    # Then I see that the value of the field that contaiend two words
    # was evaluated to an expression
    str(query).should.equal('brand:"ice cream"')


def test_query_with_field_two_words_and():
    # When I filter by field with more than one value
    query = Query(brand=(Query('ice') & Query('cream')))

    # Then I see that the value of the field that contaiend two words
    # was evaluated to an expression
    str(query).should.equal('brand:("ice" AND "cream")')


def test_query_with_field_two_words_or():
    # When I filter by field with more than one value
    query = Query(brand=(Query('ice') | Query('cream')))

    # Then I see that the value of the field that contaiend two words
    # was evaluated to an expression
    str(query).should.equal('brand:("ice" OR "cream")')


def test_query_add_boost():
    # When I filter by one word and add a boost to a field
    query = Query('stuff', _boost=('field', 3))

    # Then I see that the query contains both, the field and the query
    # boosting
    str(query).should.equal('"stuff" field^3')


def test_query_with_not():
    # When I filter by one word and add the not ~ character
    query = ~Query('ice')

    # Then I see that the value is prepended with a NOT
    str(query).should.equal('(NOT "ice")')


def test_query_with_complex_filters():
    # When I combine complex queries
    query = ~Query('cone') | Query('cream') & Query('ice')

    # Then I see that the value gives expected logical precedence
    str(query).should.equal('((NOT "cone") OR ("cream" AND "ice"))')


def test_query_with_invalid_lookup():
    # When I attempt a query with an invalid lookup
    # Then I see that it raises an exception
    Query.when.called_with(pub_date__invalid=3).should.throw(
        ParsingException,
        "This is not a valid lookup argument."
        "The valid lookups are: lte")


def test_query_with_lte_lookup():
    # When I send an lte lookup for a datetime
    query = Query(pub_date__lte=datetime(2013, 3, 13, 1, 32))

    # Then I see that the field is specified from * till the str value
    # inclusive ([])
    str(query).should.equal('pub_date:([* TO "2013-03-13T01:32:00"])')


def test_query_with_gte_lookup():
    # When I filter a gte lookup for a string
    query = Query(text__gte='cr')

    # Then I see that the field is specified from str value till *,
    # inclusive ([])
    str(query).should.equal('text:(["cr" TO *])')


def test_query_with_lt_lookup():
    # When I filter an lt look up for a string
    query = Query(text__lt='cr')

    # Then I see that the field is specified from str value till *,
    # exclusive ({})
    str(query).should.equal('text:({* TO "cr"})')


def test_query_with_gt_lookup():
    # When I filter an gt look up for a string
    query = Query(pub_date__gt=datetime(2013, 3, 13, 1, 32))

    # Then I see that the field is specified from str value till *,
    # exclusive ({})
    str(query).should.equal('pub_date:({"2013-03-13T01:32:00" TO *})')


def test_query_with_in_lookup_list():
    # When I filter an in look up for list
    query = Query(title__in=["The quick brown fox", 'The lazy dog'])

    # Then I see that the field queried over a reduced value of the list
    # with the OR operator
    str(query).should.equal('title:("The quick brown fox" OR "The lazy dog")')


def test_query_with_in_lookup_set():
    # When I filter an in look up for set
    query = Query(title__in=set(["The quick brown fox", 'The lazy dog']))

    # Then I see that the field queried over a reduced value of the set
    # with the OR operator
    str(query).should.equal('title:("The quick brown fox" OR "The lazy dog")')


def test_query_with_in_lookup_list_datetime():
    # When I filter an in look up for list with datetimes
    query = Query(pub_date__in=[datetime(2013, 3, 13, 1, 32), datetime(2013, 3, 14, 1, 0)])

    # Then I see the field queried over a reduced values of the list of datetimes converted to strings
    str(query).should.equal('pub_date:("2013-03-13T01:32:00" OR "2013-03-14T01:00:00")')


def test_query_with_range_lookup():
    # When I filter an range look up for list with datetimes
    query = Query(pub_date__range=[datetime(2013, 3, 13, 1, 32), datetime(2013, 3, 14, 1, 0)])

    # Then I see the field queried over a reduced values of the list of datetimes converted to strings
    str(query).should.equal('pub_date:("2013-03-13T01:32:00" TO "2013-03-14T01:00:00")')


def test_query_with_startswith_lookup():
    # When I filter a startswith lookup
    query = Query(title__startswith='cream')

    # Then I see the field queried with the value appended with a wildcard
    str(query).should.equal('title:("cream*")')


def test_query_with_endswith_lookup():
    # When I filter a endwith lookup
    query = Query(title__endswith='cream')

    # Then I see the field queried with the value prepended with a wildcard
    str(query).should.equal('title:("*cream")')