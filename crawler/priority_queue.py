"""
This module manages the priority queue of URLs to be crawled.
"""
from crawler import utils
from crawler.sql_models.base import DATABASE, execute_query_and_return_objects
from crawler.sql_models.job import Job

LOG = utils.get_logger(__file__)


class PriorityQueue:
    """
    Manage which URL should be crawled as next.
    """

    @staticmethod
    def get_from_random_servers_one_highest_priority_job(n_jobs: int) -> list[Job]:
        """
        Retrieves a list of jobs from the models to be crawled.

        Returns:
            list[Job]: A list of Job objects representing the URLs to be crawled.
        """
        query = f"""
SELECT j.id, j.url FROM jobs j
JOIN servers s ON j.server_id = s.id
WHERE s.is_black_list = 0
  AND j.done = 0
  AND j.url IS NOT NULL
  AND j.priority = (
    SELECT MAX(priority)
    FROM jobs
    WHERE server_id = j.server_id
      AND done = 0
      AND url IS NOT NULL
  )
ORDER BY RAND()
LIMIT {n_jobs}
"""
        return execute_query_and_return_objects(query)

    @staticmethod
    def get_one_highest_priority_job_from_each_server(n_jobs: int) -> list[Job]:
        """
        Retrieves a list of jobs from the models to be crawled.

        Returns:
            list[Job]: A list of Job objects representing the URLs to be crawled.
        """
        query = f"""
SELECT id, url
FROM (
    SELECT j.*,
        ROW_NUMBER() OVER (PARTITION BY server_id ORDER BY priority DESC) AS row_num
    FROM jobs j where j.done = 0
) as subquery
WHERE subquery.row_num = 1 
ORDER BY subquery.priority DESC 
LIMIT {n_jobs}
"""
        return execute_query_and_return_objects(query)

    def get_next_jobs(self, n_jobs: int) -> list[Job]:
        """
        Retrieves a list of jobs from the models to be crawled.

        Returns:
            list[Job]: A list of Job objects representing the URLs to be crawled.
        """
        LOG.info(f"Queue received command to obtain {n_jobs} jobs.")
        return list(PriorityQueue.get_one_highest_priority_job_from_each_server(n_jobs))
