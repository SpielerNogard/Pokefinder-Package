"""Class to create jason foamtting for logs"""
import logging
import json

class FormatterJSON(logging.Formatter):
    """Class to format Logs as Json output.
    """
    def format(self, record):
        record.message = record.getMessage()
        extra_data = record.__dict__.get('data')
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        j = {
            'levelname': record.levelname,
            'time': '%(asctime)s.%(msecs)dZ' % dict(asctime=record.asctime, msecs=record.msecs),
            'message': record.message,
            'module': record.module,
        }
        if extra_data is not None:
            j['extra_data'] = extra_data
        return json.dumps(j)

