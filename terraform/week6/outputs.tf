output "bucket_name" {
  description = "The name of the GCS bucket created"
  value       = google_storage_bucket.tf_state.name
}

output "bucket_url" {
  description = "The GCS URL for the bucket"
  value       = google_storage_bucket.tf_state.url
}

output "project_id" {
  description = "The GCP project this was deployed to"
  value       = var.project_id
}