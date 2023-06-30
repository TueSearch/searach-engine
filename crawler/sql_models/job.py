"""
This module contains the Job model. It represents a job in the crawler's queue.
"""
import urllib

import peewee
from crawler import utils
from crawler.sql_models.base import BaseModel, LongTextField, JSONField, DATABASE
from crawler.sql_models.server import Server
from crawler.relevance_classification.job_relevance import get_job_priority
from crawler.relevance_classification.url_relevance import URL

LOG = utils.get_logger(__file__)


class Job(BaseModel):
    """
    Represents a job in the crawler's queue.
    """
    id = peewee.BigAutoField(primary_key=True)
    url = LongTextField()
    server = peewee.DeferredForeignKey('servers', backref="server_id")
    parent = peewee.DeferredForeignKey('documents', backref="parent_id")
    anchor_texts = JSONField(default=[])
    anchor_texts_tokens = JSONField(default=[[]])
    priority = peewee.FloatField(default=0.0)
    being_crawled = peewee.BooleanField(default=False)
    done = peewee.BooleanField(default=False)
    success = peewee.BooleanField(default=None, null=True)

    class Meta:
        """
        Meta class for the Job model.
        """
        table_name = 'jobs'

    def __str__(self):
        return f"Job[priority={self.priority}, server={self.server}, url={self.url}]"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.url == other.url

    def __neq__(self, other):
        return self.url != other.url

    def __hash__(self):
        return hash(self.url)

    def should_be_crawled(self) -> bool:
        return self.priority > 0

    @staticmethod
    def create_jobs(relevant_links: list[URL], parent_id=None):
        if len(relevant_links) == 0:
            return
        servers = [link.server_name for link in relevant_links]
        servers = [Server.get_or_create(name=server)[0] for server in servers]
        servers = {server.name: server for server in servers}
        link_to_server = {link: servers[link.server_name] for link in relevant_links}
        for link, server in link_to_server.items():
            job = Job(url=link.url, server=server, priority=get_job_priority(server, link))
            url = job.url
            server_id = str(server.id)
            parent_id = str(parent_id) if parent_id is not None else "null"
            anchor_texts = JSONField.db(job.anchor_texts)
            anchor_texts_tokens = JSONField.db(job.anchor_texts_tokens)
            priority = str(job.priority)
            # query = f"""
            # INSERT IGNORE INTO
            # jobs (url, server_id, parent_id, anchor_texts, anchor_texts_tokens, priority)
            # VALUES ('{url}', {server_id}, {parent_id}, '{anchor_texts}', '{anchor_texts_tokens}', {priority});"""
            # print(query)
            # DATABASE.execute_sql(query)
            query = """
                INSERT INTO jobs (url, server_id, anchor_texts, anchor_texts_tokens, priority)
                VALUES (%s, %s, %s, %s, %s);
            """
            params = (
                url,
                server_id,
                anchor_texts,
                anchor_texts_tokens,
                priority
            )
            print(params)
            DATABASE.execute_sql(query, params)
