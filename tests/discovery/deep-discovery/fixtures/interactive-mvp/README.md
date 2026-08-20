# Relay Lens

Relay Lens is an internal MVP used by operations managers to upload carrier documents, extract shipment facts, and review normalized results. The API accepts uploads and exposes completed results. A background worker performs extraction.

Document processing is used in weekly operations reviews. CSV export exists in the API but is incomplete. A billing adapter was started during an experiment and is not part of the current product.

Production runs on a small container host maintained outside the company's standard cloud tenancy. The runtime file in this repository references secrets and DNS configuration in an adjacent `platform-config` repository that is not included here.

The product sponsor is the VP of Operations. Sean Kim owns the business workflow. Maya Chen is the primary engineer.
