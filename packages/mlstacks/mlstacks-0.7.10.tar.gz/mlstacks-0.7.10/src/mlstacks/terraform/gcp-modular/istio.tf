# create kserve module
module "istio" {
  source = "../modules/istio-module"

  count = (var.enable_model_deployer_kserve || var.enable_model_deployer_seldon) ? 1 : 0

  depends_on = [
    google_container_cluster.gke,
    null_resource.configure-local-kubectl,
  ]

  chart_version = local.istio.version
}
