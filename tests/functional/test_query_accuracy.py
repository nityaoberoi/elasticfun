from sure import expect

from . import helper

from elasticfun import Query


# def test_query_all():
#     # Given that we have a list of indexed documents saved on an empty
#     # elasticsearch instance
#     helper.flush('default')
#     helper.index('default', 'person', {"name": "Joe Tester"})
#     helper.index('default', 'person', {"name": "Jessica Coder"})
#     helper.refresh('default')

#     # When I search for Joe
#     results = helper.search(Query())

#     # Then I see that the results matched our expectation
#     results.should.equal([
#         {"name": "Joe Tester"},
#         {"name": "Jessica Coder"}
#     ])


def test_query_single_word_no_results():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for something that does NOT exist in ES
    results = helper.search(Query('something'))

    # Then I see that the results are empty
    results.should.be.empty


def test_query_single_word():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('joe'))

    # Then I see that the results matched our expectation
    results.should.equal([{"name": "Joe Tester"}])


def test_query_single_field_no_results():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for something that does NOT exist
    results = helper.search(Query(name='something'))

    # Then I see that the results were empty
    results.should.be.empty


def test_query_single_field():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query(name='jessica'))

    # Then I see that the results matched our expectation
    results.should.equal([{"name": "Jessica Coder"}])


def test_query_single_correct_field():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query(name='jessica'))

    # Then I see that the results matched our expectation
    results.should.equal([
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])


def test_query_with_and():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('jessica') & Query('coder'))

    # Then I see that the results matched our expectation
    results.should.equal([{"name": "Jessica Coder"}])


def test_query_with_and_all_words_crossfield():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('jessica') & Query('coder'))

    # Then I see that the results matched our expectations
    # This is the only result since all are single values
    # enclosed within quotes
    results.should.equal([
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])


def test_query_with_and_across_fields():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('jessica') & Query('Worker'))

    # Then I see that the results matched our expectation
    results.should.equal([
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])


def test_query_with_or():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index('default', 'person', {"name": "Joe Tester"})
    helper.index('default', 'person', {"name": "Jessica Coder"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('jessica') | Query('coder'))

    # Then I see that the results matched our expectation
    results.should.equal([{"name": "Jessica Coder"}])


def test_query_with_or_all_words_crossfield():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe
    results = helper.search(Query('jessica') | Query('coder'))

    # Then I see that the results matched our expectations
    # This is the only result since all are single values
    # enclosed within quotes
    expect(results).to.equal([
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"},
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"}
    ])


def test_query_with_or_across_fields():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe or worker
    results = helper.search(Query('joe') | Query('Worker'))

    # Then I see that the results matched our expectation
    expect(results).to.equal([
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"},
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"}
    ])


def test_query_with_two_words():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica noncoder
    results = helper.search(Query('jessica noncoder'))

    # Then I see that the results matched our expectation
    results.should.equal([
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"},
    ])


def test_query_with_two_words_no_result():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for Joe or worker
    results = helper.search(Query('jessica lincoln'))

    # Then I see that the results should be empty
    results.should.be.empty


def test_query_with_field_two_words():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica coder
    results = helper.search(Query(name='jessica coder'))

    # Then I see that the results matched our expectation
    results.should.equal([
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])


def test_query_with_field_two_words_no_result():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica coder
    results = helper.search(Query(sibling='jessica coder'))

    # Then I see that the results should be empty
    results.should.be.empty


def test_query_with_field_two_words_and():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica coder
    results = helper.search(Query(name=(Query('jessica') & Query('coder'))))

    # Then I see that the results matched our expectation
    results.should.equal([
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])


def test_query_with_field_two_words_and_no_result():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica coder
    results = helper.search(Query(name=(Query('jessica') & Query('worker'))))

    # Then I see that the results should be empty
    results.should.be.empty


def test_query_with_field_two_words_or():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica coder
    results = helper.search(Query(name=(Query('jessica') | Query('joe'))))

    # Then I see that the results matched our expectation
    expect(results).to.equal([
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"},
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])


def test_query_with_field_two_words_or_no_result():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica coder
    results = helper.search(Query(name=(Query('jess') | Query('worker'))))

    # Then I see that the results should be empty
    results.should.be.empty


def test_query_with_and_two_fields():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica coder
    results = helper.search(Query(name='jessica') & Query(sibling='lincoln'))

    # Then I see that the results matched our expectation
    expect(results).to.equal([
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])


def test_query_with_or_two_fields():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for jessica coder
    results = helper.search(Query(name='jessica') | Query(sibling='jessica'))

    # Then I see that the results matched our expectation
    expect(results).to.equal([
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"},
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])


def test_query_with_not():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.refresh('default')

    # When I search for query with no jessica
    results = helper.search(~Query('jessica'))

    # Then I see that the results matched our expectation
    results.should.be.empty


def test_query_with_complex_and_or_not():
    # Given that we have a list of indexed documents saved on an empty
    # elasticsearch instance
    helper.flush('default')
    helper.index(
        'default', 'person',
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"})
    helper.index(
        'default', 'person',
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"})
    helper.index(
        'default', 'person',
        {"name": "Emily Author", 'sibling': "Tim Worker"})
    helper.refresh('default')

    # When I search for query with no jessica
    results = helper.search(~Query('Emily') & Query(name='joe') | Query(sibling='worker'))

    # Then I see that the results matched our expectation
    expect(results).to.equal([
        {"name": "Joe Tester", 'sibling': "Jessica Noncoder"},
        {"name": "Jessica Coder", 'sibling': "Lincoln Worker"}
    ])

# Missing tests for boost and lookups