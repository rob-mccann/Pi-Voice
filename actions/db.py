#!/usr/bin/env python
# coding: utf-8

"""
Main script for dbpedia quepy.
"""

import sys
import time
import random
import datetime

import quepy
from SPARQLWrapper import SPARQLWrapper, JSON
from ex.exception import NoResultsFoundException

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
dbpedia = quepy.install("actions.dbpedia")


class DBPedia:
    def __init__(self, tts):
            self.tts = tts

    def process(self, job):
        if job.get_is_processed():
            return False

        try:
            self.query(job.raw())
            job.is_processed = True
        except NoResultsFoundException:
            print "failed to get reponse from dbpedia"
            return False

    def query(self, phrase):
        print "Creating SparQL query"

        target, query, metadata = dbpedia.get_query(phrase)

        if isinstance(metadata, tuple):
            query_type = metadata[0]
            metadata = metadata[1]
        else:
            query_type = metadata
            metadata = None

        if query is None:
            raise NoResultsFoundException()

        print query

        print_handlers = {
            "define": self.print_define,
            "enum": self.print_enum,
            "time": self.print_time,
            "literal": self.print_literal,
            "age": self.print_age,
        }

        if target.startswith("?"):
            target = target[1:]

        if query:
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            if not results["results"]["bindings"]:
                raise NoResultsFoundException()

        return print_handlers[query_type](results, target, metadata)

    def print_define(self, results, target, metadata=None):
        for result in results["results"]["bindings"]:
            if result[target]["xml:lang"] == "en":
                self.say(result[target]["value"])

    def print_enum(self, results, target, metadata=None):
        used_labels = []

        for result in results["results"]["bindings"]:
            if result[target]["type"] == u"literal":
                if result[target]["xml:lang"] == "en":
                    label = result[target]["value"]
                    if label not in used_labels:
                        used_labels.append(label)
                        self.say(label)


    def print_literal(self, results, target, metadata=None):
        for result in results["results"]["bindings"]:
            literal = result[target]["value"]
            if metadata:
                self.say(metadata.format(literal))
            else:
                self.say(literal)


    def print_time(self, results, target, metadata=None):
        gmt = time.mktime(time.gmtime())
        gmt = datetime.datetime.fromtimestamp(gmt)

        for result in results["results"]["bindings"]:
            offset = result[target]["value"].replace(u"−", u"-")

            if "to" in offset:
                from_offset, to_offset = offset.split("to")
                from_offset, to_offset = int(from_offset), int(to_offset)

                if from_offset > to_offset:
                    from_offset, to_offset = to_offset, from_offset

                from_delta = datetime.timedelta(hours=from_offset)
                to_delta = datetime.timedelta(hours=to_offset)

                from_time = gmt + from_delta
                to_time = gmt + to_delta

                location_string = random.choice(["where you are",
                                                 "your location"])

                self.say("Between %s and %s, depending %s" % \
                      (from_time.strftime("%H:%M"),
                       to_time.strftime("%H:%M on %A"),
                       location_string))

            else:
                offset = int(offset)

                delta = datetime.timedelta(hours=offset)
                the_time = gmt + delta

                self.say(the_time.strftime("%H:%M on %A"))


    def print_age(self, results, target, metadata=None):
        assert len(results["results"]["bindings"]) == 1

        birth_date = results["results"]["bindings"][0][target]["value"]
        year, month, days = birth_date.split("-")

        birth_date = datetime.date(int(year), int(month), int(days))

        now = datetime.datetime.utcnow()
        now = now.date()

        age = now - birth_date
        self.say("{} years old".format(age.days / 365))

    def say(self, text):
        return self.tts.say(text)
