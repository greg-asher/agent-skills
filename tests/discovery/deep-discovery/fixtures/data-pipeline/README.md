# Usage Exporter

Usage Exporter is a scheduled internal application. Every morning it normalizes the previous day's metering rows, aggregates usage by customer account, and delivers a CSV to Finance.

The daily export is active. A retry dashboard is described in an old planning note but has not been built. Finance owns the output; Data Engineering maintains the job.
