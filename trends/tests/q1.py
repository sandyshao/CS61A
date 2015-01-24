test = {
  'names': [
    'q1',
    '1'
  ],
  'params': {
    'doctest': {
      'cache': """
      # Storing original implementation of ADTs
      trends.position_adt = (make_position, latitude, longitude)
      """
    }
  },
  'points': 1,
  'suites': [
    [
      {
        'locked': True,
        'test': """
        >>> t = make_tweet('just ate lunch', datetime(2014, 9, 29, 13), 122, 37)
        >>> tweet_text(t)
        b087e917903af5de2907da21d8a6e66b
        # locked
        # choice: datetime(2014, 9, 29, 13, 0)
        # choice: 'just ate lunch'
        # choice: 122
        # choice: '"just ate lunch" @ (122, 37)'
        >>> tweet_time(t)
        de00f35e58ac443ac754ff476b6dc95a
        # locked
        # choice: datetime(2014, 9, 29, 13, 0)
        # choice: 'just ate lunch'
        # choice: 122
        # choice: '"just ate lunch" @ (122, 37)'
        >>> latitude(tweet_location(t))
        d2d351dd10109bcfaf1d4dbcdc9cecc2
        # locked
        # choice: datetime(2014, 9, 29, 13, 0)
        # choice: 'just ate lunch'
        # choice: 122
        # choice: '"just ate lunch" @ (122, 37)'
        >>> tweet_string(t)
        972f6fa56abb0c903cf9e15e7f2bddb6
        # locked
        # choice: datetime(2014, 9, 29, 13, 0)
        # choice: 'just ate lunch'
        # choice: 122
        # choice: '"just ate lunch" @ (122, 37)'
        """,
        'type': 'doctest'
      },
      {
        'never_lock': True,
        'test': """
        >>> s = make_tweet_fn('just ate lunch', datetime(2014, 9, 29, 13), 122, 37)
        >>> tweet_text_fn(s)
        'just ate lunch'
        >>> tweet_time_fn(s)
        datetime(2014, 9, 29, 13, 0)
        >>> latitude(tweet_location_fn(s))
        122
        """,
        'type': 'doctest'
      },
      {
        'never_lock': True,
        'teardown': """
        # restore original position ADT
        trends.make_position, trends.latitude, trends.longitude = trends.position_adt
        """,
        'test': """
        >>> # Testing for abstraction violations
        >>> trends.make_position = Position
        >>> trends.latitude = Position.latitude
        >>> trends.longitude = Position.longitude
        >>> f = make_tweet('first!', datetime(2014, 9, 20, 13), 122, 37)
        >>> tweet_text(f)
        'first!'
        >>> tweet_time(f)
        datetime(2014, 9, 20, 13, 0)
        >>> trends.latitude(tweet_location(f))
        122
        """,
        'type': 'doctest'
      }
    ]
  ]
}