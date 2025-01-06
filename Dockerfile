FROM apache/airflow:2.10.3
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


# Download the Redshift JDBC driver for DataFrame-based export
RUN curl -LO https://s3.amazonaws.com/redshift-downloads/drivers/jdbc/2.1.0.28/redshift-jdbc42-2.1.0.28.jar && \
    mkdir -p /usr/local/share/java && \
    mv redshift-jdbc42-2.1.0.28.jar /usr/local/share/java/redshift-jdbc.jar

# Switch back to airflow user
USER airflow

# Install necessary Python packages
RUN pip install --no-cache-dir \
    boto3 \
    openai \
    redshift_connector \
    pandas \
    python-dotenv \
    praw \
    pyarrow

# Set the CLASSPATH for JDBC driver to ensure it’s accessible for Redshift export
ENV CLASSPATH="/usr/local/share/java/redshift-jdbc.jar"
