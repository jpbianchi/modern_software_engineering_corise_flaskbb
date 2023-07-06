terraform {
  backend "s3" {
    bucket = "terraform-state-flaskbb-jpb"
    key    = "core/terraform.tfstate"
    region = "eu-west-3"
  }
}
