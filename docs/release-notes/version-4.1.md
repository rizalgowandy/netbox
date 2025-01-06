# NetBox v4.1

## v4.1.10 (2024-12-23)

### Bug Fixes

* [#18260](https://github.com/netbox-community/netbox/issues/18260) - Fix object change logging

---

## v4.1.9 (2024-12-17)

!!! danger "Do Not Use"
    This release contains a regression which breaks change logging. Please use release v4.1.10 instead.

### Enhancements

* [#17215](https://github.com/netbox-community/netbox/issues/17215) - Change the highlighted color of disabled interfaces in interface lists
* [#18224](https://github.com/netbox-community/netbox/issues/18224) - Apply all registered request processors when running custom scripts

### Bug Fixes

* [#16757](https://github.com/netbox-community/netbox/issues/16757) - Fix rendering of IP addresses table when assigning an existing IP address to an interface with global HTMX navigation enabled
* [#17868](https://github.com/netbox-community/netbox/issues/17868) - Fix `ZeroDivisionError` exception under specific circumstances when generating a cable trace
* [#18124](https://github.com/netbox-community/netbox/issues/18124) - Enable referencing cable attributes when querying a `cabletermination_set` via the GraphQL API
* [#18230](https://github.com/netbox-community/netbox/issues/18230) - Fix `AttributeError` exception when attempting to edit an IP address assigned to a virtual machine interface

---

## v4.1.8 (2024-12-12)

### Enhancements

* [#17071](https://github.com/netbox-community/netbox/issues/17071) - Enable OOB IP address designation during bulk import
* [#17465](https://github.com/netbox-community/netbox/issues/17465) - Enable designation of rack type during bulk import & bulk edit
* [#17889](https://github.com/netbox-community/netbox/issues/17889) - Enable designating an IP address as out-of-band for a device upon creation
* [#17960](https://github.com/netbox-community/netbox/issues/17960) - Add L2TP, PPTP, Wireguard, and OpenVPN tunnel types
* [#18021](https://github.com/netbox-community/netbox/issues/18021) - Automatically clear cache on restart when `DEBUG` is enabled
* [#18061](https://github.com/netbox-community/netbox/issues/18061) - Omit stack trace from rendered device/VM configuration when an exception is raised
* [#18065](https://github.com/netbox-community/netbox/issues/18065) - Include status in device details when hovering on rack elevation
* [#18211](https://github.com/netbox-community/netbox/issues/18211) - Enable the dynamic registration of context managers for request processing

### Bug Fixes

* [#14044](https://github.com/netbox-community/netbox/issues/14044) - Fix unhandled AttributeError exception when bulk renaming objects
* [#17490](https://github.com/netbox-community/netbox/issues/17490) - Fix dynamic inclusion support for config templates
* [#17810](https://github.com/netbox-community/netbox/issues/17810) - Fix validation of racked device fields when modifying via REST API
* [#17820](https://github.com/netbox-community/netbox/issues/17820) - Ensure default custom field values are populated when creating new modules
* [#18044](https://github.com/netbox-community/netbox/issues/18044) - Show plugin-generated alerts within UI views for custom scripts
* [#18150](https://github.com/netbox-community/netbox/issues/18150) - Fix REST API pagination for low `MAX_PAGE_SIZE` values
* [#18183](https://github.com/netbox-community/netbox/issues/18183) - Omit UI navigation bar when printing
* [#18213](https://github.com/netbox-community/netbox/issues/18213) - Fix searching for ASN ranges by name

---

## v4.1.7 (2024-11-21)

### Enhancements

* [#15239](https://github.com/netbox-community/netbox/issues/15239) - Enable adding/removing individual VLANs while bulk editing device interfaces
* [#17871](https://github.com/netbox-community/netbox/issues/17871) - Enable the assignment/removal of virtualization cluster via device bulk edit
* [#17934](https://github.com/netbox-community/netbox/issues/17934) - Add 1000Base-LX interface type
* [#18007](https://github.com/netbox-community/netbox/issues/18007) - Hide sensitive parameters under data source view (even for privileged users)

### Bug Fixes

* [#17459](https://github.com/netbox-community/netbox/issues/17459) - Correct help text on `name` field of module type component templates
* [#17901](https://github.com/netbox-community/netbox/issues/17901) - Ensure GraphiQL UI resources are served locally
* [#17921](https://github.com/netbox-community/netbox/issues/17921) - Fix scheduling of recurring custom scripts
* [#17923](https://github.com/netbox-community/netbox/issues/17923) - Fix the execution of custom scripts via REST API & management command
* [#17963](https://github.com/netbox-community/netbox/issues/17963) - Fix selection of all listed objects during bulk edit
* [#17969](https://github.com/netbox-community/netbox/issues/17969) - Fix system info export when a config revision exists
* [#17972](https://github.com/netbox-community/netbox/issues/17972) - Force evaluation of `LOGIN_REQUIRED` when requesting static media
* [#17986](https://github.com/netbox-community/netbox/issues/17986) - Correct labels for virtual machine & virtual disk size properties
* [#18037](https://github.com/netbox-community/netbox/issues/18037) - Fix validation of maximum VLAN ID value when defining VLAN groups
* [#18038](https://github.com/netbox-community/netbox/issues/18038) - The `to_grams()` utility function should always return an integer value

---

## v4.1.6 (2024-10-31)

### Bug Fixes

* [#17700](https://github.com/netbox-community/netbox/issues/17700) - Fix warning when no scripts are found within a script module
* [#17884](https://github.com/netbox-community/netbox/issues/17884) - Fix translation support for certain tab headings
* [#17885](https://github.com/netbox-community/netbox/issues/17885) - Fix regression preventing custom scripts from executing

## v4.1.5 (2024-10-28)

### Enhancements

* [#17789](https://github.com/netbox-community/netbox/issues/17789) - Provide a single "scope" field for bulk editing VLAN group scope assignments

### Bug Fixes

* [#17358](https://github.com/netbox-community/netbox/issues/17358) - Fix validation of overlapping IP ranges
* [#17374](https://github.com/netbox-community/netbox/issues/17374) - Fix styling of highlighted table rows in dark mode
* [#17460](https://github.com/netbox-community/netbox/issues/17460) - Ensure bulk action buttons are consistent for device type components
* [#17635](https://github.com/netbox-community/netbox/issues/17635) - Ensure AbortTransaction is caught when running a custom script with `commit=False`
* [#17685](https://github.com/netbox-community/netbox/issues/17685) - Ensure background jobs are validated before being scheduled
* [#17710](https://github.com/netbox-community/netbox/issues/17710) - Remove cached fields on CableTermination model from GraphQL API
* [#17740](https://github.com/netbox-community/netbox/issues/17740) - Ensure support for image attachments with a `.webp` file extension
* [#17749](https://github.com/netbox-community/netbox/issues/17749) - Restore missing `devicetypes` and `children` fields for several objects in GraphQL API
* [#17754](https://github.com/netbox-community/netbox/issues/17754) - Remove paginator from version history table under plugin view
* [#17759](https://github.com/netbox-community/netbox/issues/17759) - Retain `job_timeout` value when scheduling a recurring custom script
* [#17774](https://github.com/netbox-community/netbox/issues/17774) - Fix SSO login support for Entra ID (formerly Azure AD)
* [#17802](https://github.com/netbox-community/netbox/issues/17802) - Fix background color for bulk rename buttons in list views
* [#17838](https://github.com/netbox-community/netbox/issues/17838) - Adjust `manage.py` to reference `python3` executable

---

## v4.1.4 (2024-10-15)

### Enhancements

* [#11671](https://github.com/netbox-community/netbox/issues/11671) - Display device's rack position in cable traces
* [#15829](https://github.com/netbox-community/netbox/issues/15829) - Rename Microsoft Azure AD SSO backend to Microsoft Entra ID
* [#16009](https://github.com/netbox-community/netbox/issues/16009) - Float form & bulk operation buttons within UI
* [#17079](https://github.com/netbox-community/netbox/issues/17079) - Introduce additional choices for device airflow direction
* [#17216](https://github.com/netbox-community/netbox/issues/17216) - Add EVPN-VPWS L2VPN type
* [#17655](https://github.com/netbox-community/netbox/issues/17655) - Limit the display of tagged VLANs within interface tables
* [#17669](https://github.com/netbox-community/netbox/issues/17669) - Enable filtering VLANs by assigned device or VM interface

### Bug Fixes

* [#16024](https://github.com/netbox-community/netbox/issues/16024) - Fix AND/OR filtering in GraphQL API for selection fields
* [#17400](https://github.com/netbox-community/netbox/issues/17400) - Fix cable tracing across split paths
* [#17562](https://github.com/netbox-community/netbox/issues/17562) - Fix GraphQL API query support for custom field choices
* [#17566](https://github.com/netbox-community/netbox/issues/17566) - Fix AttributeError exception resulting from background jobs with no associated object type
* [#17614](https://github.com/netbox-community/netbox/issues/17614) - Disallow removal of a master device from its virtual chassis
* [#17636](https://github.com/netbox-community/netbox/issues/17636) - Fix filtering of related objects when adding a power port, rear port, or inventory item template to a device type
* [#17644](https://github.com/netbox-community/netbox/issues/17644) - Correct sizing of logo & SSO icons on login page
* [#17648](https://github.com/netbox-community/netbox/issues/17648) - Fix AttributeError exception when attempting to delete a background job under certain conditions
* [#17663](https://github.com/netbox-community/netbox/issues/17663) - Fix extended lookups for choice field filters
* [#17671](https://github.com/netbox-community/netbox/issues/17671) - Fix the display of rack types in global search results
* [#17713](https://github.com/netbox-community/netbox/issues/17713) - Fix UnboundLocalError exception when attempting to sync data source in parallel

---

## v4.1.3 (2024-10-02)

### Enhancements

* [#17639](https://github.com/netbox-community/netbox/issues/17639) - Add SOCKS support to proxy settings for Git remote data sources

### Bug Fixes

* [#17558](https://github.com/netbox-community/netbox/issues/17558) - Raise validation error when attempting to remove a custom field choice in use

---

## v4.1.2 (2024-09-26)

### Enhancements

* [#14201](https://github.com/netbox-community/netbox/issues/14201) - Enable global search for AS numbers using "AS" prefix
* [#15408](https://github.com/netbox-community/netbox/issues/15408) - Enable bulk import of primary IPv4 & IPv6 addresses for virtual device contexts (VDCs)
* [#16781](https://github.com/netbox-community/netbox/issues/16781) - Add 100Base-X SFP interface type
* [#17255](https://github.com/netbox-community/netbox/issues/17255) - Include return URL when creating new IP address from prefix IPs list
* [#17471](https://github.com/netbox-community/netbox/issues/17471) - Add Eaton C39 power outlet type
* [#17482](https://github.com/netbox-community/netbox/issues/17482) - Do not preload Branch & StagedChange models in `nbshell`
* [#17550](https://github.com/netbox-community/netbox/issues/17550) - Add IEEE 802.15.4 wireless interface type

### Bug Fixes

* [#16837](https://github.com/netbox-community/netbox/issues/16837) - Fix filtering of cables with no type assigned
* [#17083](https://github.com/netbox-community/netbox/issues/17083) - Trim clickable area of form field labels
* [#17126](https://github.com/netbox-community/netbox/issues/17126) - Show total device weight in both imperial & metric units
* [#17360](https://github.com/netbox-community/netbox/issues/17360) - Fix AttributeError under child object views when experimental HTMX navigation is enabled
* [#17406](https://github.com/netbox-community/netbox/issues/17406) - Fix the cleanup of stale custom field data after removing a plugin
* [#17419](https://github.com/netbox-community/netbox/issues/17419) - Rebuild MPTT for module bays on upgrade to v4.1
* [#17492](https://github.com/netbox-community/netbox/issues/17492) - Fix URL resolution in `NetBoxModelSerializer` for plugin models
* [#17497](https://github.com/netbox-community/netbox/issues/17497) - Fix uncaught FieldError exception when referencing an invalid field on a related object during bulk import
* [#17498](https://github.com/netbox-community/netbox/issues/17498) - Fix MultipleObjectsReturned exception when importing a device type without uniquely specifying a manufacturer
* [#17501](https://github.com/netbox-community/netbox/issues/17501) - Fix reporting of last run time & status for custom scripts under UI
* [#17511](https://github.com/netbox-community/netbox/issues/17511) - Restore consistent font support for non-Latin characters
* [#17517](https://github.com/netbox-community/netbox/issues/17517) - Fix cable termination selection after switching termination type
* [#17521](https://github.com/netbox-community/netbox/issues/17521) - Correct text color in notification pop-ups under dark mode
* [#17522](https://github.com/netbox-community/netbox/issues/17522) - Fix language translation of form field labels under user preferences
* [#17537](https://github.com/netbox-community/netbox/issues/17537) - Fix global search support for ASN range names
* [#17555](https://github.com/netbox-community/netbox/issues/17555) - Fix toggling disconnected interfaces under device view
* [#17601](https://github.com/netbox-community/netbox/issues/17601) - Record change to terminating object when disconnecting a cable
* [#17605](https://github.com/netbox-community/netbox/issues/17605) - Fix calculation of aggregate VM disk space under cluster view
* [#17611](https://github.com/netbox-community/netbox/issues/17611) - Correct custom field minimum value validation error message

---

## v4.1.1 (2024-09-12)

### Enhancements

* [#16926](https://github.com/netbox-community/netbox/issues/16926) - Add USB front & rear port types
* [#17347](https://github.com/netbox-community/netbox/issues/17347) - Add NEMA L22-20 power port & outlet types

### Bug Fixes

* [#17066](https://github.com/netbox-community/netbox/issues/17066) - Fix OpenAPI schema definition for custom scripts REST API endpoint
* [#17332](https://github.com/netbox-community/netbox/issues/17332) - Restore pagination for object list dashboard widgets
* [#17333](https://github.com/netbox-community/netbox/issues/17333) - Avoid prefetching all jobs when retrieving custom scripts via the REST API
* [#17353](https://github.com/netbox-community/netbox/issues/17353) - Fix styling of map buttons under site and device views
* [#17354](https://github.com/netbox-community/netbox/issues/17354) - Prevent object & multi-object custom fields from breaking bulk import forms
* [#17362](https://github.com/netbox-community/netbox/issues/17362) - Remove duplicate prefixes & IP addresses returned by the `present_in_vrf` query filter
* [#17364](https://github.com/netbox-community/netbox/issues/17364) - Fix rendering of Markdown tables inside object list dashboard widgets
* [#17387](https://github.com/netbox-community/netbox/issues/17387) - Fix display of the changelog tab for users with sufficient permission
* [#17410](https://github.com/netbox-community/netbox/issues/17410) - Enable debug toolbar middleware for `strawberry-django` only when `DEBUG` is true
* [#17414](https://github.com/netbox-community/netbox/issues/17414) - Fix support for declaring individual VLAN IDs within a VLAN group
* [#17431](https://github.com/netbox-community/netbox/issues/17431) - Fix database migration error when upgrading to v4.1 from v3.7 or earlier
* [#17437](https://github.com/netbox-community/netbox/issues/17437) - Fix exception when specifying a bridge relationship on an interface template
* [#17444](https://github.com/netbox-community/netbox/issues/17444) - Custom script fails to execute when triggered by an event rule
* [#17457](https://github.com/netbox-community/netbox/issues/17457) - GraphQL `service_list` filter should not require a port number

---

## v4.1.0 (2024-09-03)

### Breaking Changes

* Several filters deprecated in v4.0 have been removed (see [#15410](https://github.com/netbox-community/netbox/issues/15410)).
* The unit size for `VirtualMachine.disk` and `VirtualDisk.size` has been changed from 1 gigabyte to 1 megabyte. Existing values will be adjusted automatically during the upgrade process.
* The `min_vid` and `max_vid` fields on the VLAN group model have been replaced with `vid_ranges`, an array of starting and ending VLAN ID pairs.
* The five individual event type fields on the EventRule model have been replaced by a single `event_types` array field, which lists applicable event types by name.
* All UI views & API endpoints associated with change records have been moved from `/extras` to `/core`.
* The `validate()` method on CustomValidator subclasses now **must** accept the request argument (deprecated in v4.0 by [#14279](https://github.com/netbox-community/netbox/issues/14279/)).

### New Features

#### Circuit Groups ([#7025](https://github.com/netbox-community/netbox/issues/7025))

Circuits can now be assigned to groups for administrative purposes. Each circuit may be assigned to multiple groups, and each assignment may optionally indicate a priority (primary, secondary, or tertiary).

#### VLAN Group ID Ranges ([#9627](https://github.com/netbox-community/netbox/issues/9627))

The VLAN group model has been enhanced to support multiple VLAN ID (VID) ranges, whereas previously it could track only a single beginning and ending VID pair. VID ranges are stored as an array of beginning and ending (inclusive) integer pairs, e.g. `1-100,1000-1999`.

#### Nested Device Modules ([#10500](https://github.com/netbox-community/netbox/issues/10500))

Module bays can now be added to modules to effect a hierarchical arrangement of submodules within a device. A module installed within a device's module bay may itself have module bays into which child modules may be installed.

#### Rack Types ([#12826](https://github.com/netbox-community/netbox/issues/12826))

A new rack type model has been introduced, which functions similarly to device types. Users can now define a common make and model of equipment rack, the attributes of which are automatically populated when creating a new rack of that type. Backward compatibility for racks with individually defined characteristics is fully retained.

#### Plugins Catalog Integration ([#14731](https://github.com/netbox-community/netbox/issues/14731))

The NetBox UI now integrates directly with the canonical [plugins catalog](https://netboxlabs.com/netbox-plugins/) hosted by [NetBox Labs](https://netboxlabs.com). Users can now explore available plugins and check for newer releases natively within the NetBox user interface.

#### User Notifications ([#15621](https://github.com/netbox-community/netbox/issues/15621))

NetBox now includes a user notification system. Users can subscribe to individual objects and be alerted to changes within the web interface. Additionally, event rules can be created to trigger notifications for specific users and/or groups. Plugins can also employ this notification system for their own purposes.

### Enhancements

* [#7537](https://github.com/netbox-community/netbox/issues/7537) - Add a serial number field for virtual machines
* [#8198](https://github.com/netbox-community/netbox/issues/8198) - Enable uniqueness enforcement for custom field values
* [#8984](https://github.com/netbox-community/netbox/issues/8984) - Enable filtering of custom script output by log level
* [#11969](https://github.com/netbox-community/netbox/issues/11969) - Support for tracking airflow on racks and module types
* [#14656](https://github.com/netbox-community/netbox/issues/14656) - Dynamically render the custom field edit form depending on the selected field type
* [#15106](https://github.com/netbox-community/netbox/issues/15106) - Add `distance` and `distance_unit` fields for wireless links
* [#15156](https://github.com/netbox-community/netbox/issues/15156) - Add `display_url` field to all REST API serializers, which links to the corresponding UI view for an object
* [#16574](https://github.com/netbox-community/netbox/issues/16574) - Add `last_synced` time to REST API serializer for data sources
* [#16580](https://github.com/netbox-community/netbox/issues/16580) - Enable plugin views to enforce `LOGIN_REQUIRED` selectively (remove `AUTH_EXEMPT_PATHS`)
* [#16782](https://github.com/netbox-community/netbox/issues/16782) - Enable filtering of selection choices for object and multi-object custom fields
* [#16907](https://github.com/netbox-community/netbox/issues/16907) - Update user interface styling
* [#17051](https://github.com/netbox-community/netbox/issues/17051) - Introduce `ISOLATED_DEPLOYMENT` config parameter for denoting Internet isolation
* [#17221](https://github.com/netbox-community/netbox/issues/17221) - `ObjectEditView` now supports HTMX-based object editing
* [#17288](https://github.com/netbox-community/netbox/issues/17288) - Introduce a configurable limit on the number of aliases within a GraphQL API request
* [#17289](https://github.com/netbox-community/netbox/issues/17289) - Enforce a standard policy for local passwords by default
* [#17318](https://github.com/netbox-community/netbox/issues/17318) - Include the assigned provider in nested API representation of circuits

### Bug Fixes (From Beta1)

* [#17086](https://github.com/netbox-community/netbox/issues/17086) - Fix exception when viewing a job with no related object
* [#17097](https://github.com/netbox-community/netbox/issues/17097) - Record static object representation when calling `NotificationGroup.notify()`
* [#17098](https://github.com/netbox-community/netbox/issues/17098) - Prevent automatic deletion of related notifications when deleting an object
* [#17159](https://github.com/netbox-community/netbox/issues/17159) - Correct file paths in plugin installation instructions
* [#17163](https://github.com/netbox-community/netbox/issues/17163) - Fix filtering of related services under IP address view
* [#17169](https://github.com/netbox-community/netbox/issues/17169) - Avoid duplicating catalog listings for installed plugins
* [#17301](https://github.com/netbox-community/netbox/issues/17301) - Correct styling of the edit & delete buttons for custom script modules
* [#17302](https://github.com/netbox-community/netbox/issues/17302) - Fix log level filtering support for custom script messages
* [#17306](https://github.com/netbox-community/netbox/issues/17306) - Correct rounding of reported VLAN group utilization

### Plugins

* [#15692](https://github.com/netbox-community/netbox/issues/15692) - Introduce improved plugin support for background jobs
* [#16359](https://github.com/netbox-community/netbox/issues/16359) - Enable plugins to embed content in the top navigation bar
* [#16726](https://github.com/netbox-community/netbox/issues/16726) - Extend `PluginTemplateExtension` to enable registering multiple models
* [#16776](https://github.com/netbox-community/netbox/issues/16776) - Add an `alerts()` method to `PluginTemplateExtension` for embedding important information on object views
* [#16886](https://github.com/netbox-community/netbox/issues/16886) - Introduce a mechanism for plugins to register custom event types (for use with user notifications)

### Other Changes

* [#14692](https://github.com/netbox-community/netbox/issues/14692) - Change the atomic unit for virtual disks from 1GB to 1MB
* [#14861](https://github.com/netbox-community/netbox/issues/14861) - The URL path for UI views concerning virtual disks has been standardized to `/virtualization/virtual-disks/`
* [#15410](https://github.com/netbox-community/netbox/issues/15410) - Remove various deprecated query filters
* [#15908](https://github.com/netbox-community/netbox/issues/15908) - Indicate product edition in release data
* [#16388](https://github.com/netbox-community/netbox/issues/16388) - Move all change logging resources from `extras` to `core`
* [#16884](https://github.com/netbox-community/netbox/issues/16884) - Remove the ID column from the default table configuration for changelog records
* [#16988](https://github.com/netbox-community/netbox/issues/16988) - Relocate rack items in navigation menu
* [#17143](https://github.com/netbox-community/netbox/issues/17143) - The use of legacy "nested" serializer classes has been deprecated

### REST API Changes

* The `/api/extras/object-changes/` endpoint has moved to `/api/core/object-changes/`.
* Most object representations now include a read-only `display_url` field, which links to the object's corresponding UI view.
* Added the following endpoints:
    * `/api/circuits/circuit-groups/`
    * `/api/circuits/circuit-group-assignments/`
    * `/api/dcim/rack-types/`
    * `/api/extras/notification-groups/`
    * `/api/extras/notifications/`
    * `/api/extras/subscriptions/`
* circuits.Circuit
    * Added the `assignments` field, which lists all group assignments
* core.DataSource
    * Added the read-only `last_synced` field
* dcim.ModuleBay
    * Added the optional `module` foreign key field
* dcim.ModuleBayTemplate
    * Added the optional `module_type` foreign key field
* dcim.ModuleType
    * Added the optional `airflow` choice field
* dcim.Rack
    * Added the optional `rack_type` foreign key field
    * Added the optional `airflow` choice field
* extras.CustomField
    * Added the `related_object_filter` JSON field for object and multi-object custom fields
    * Added the `validation_unique` boolean field
* extras.EventRule
    * Removed the `type_create`, `type_update`, `type_delete`, `type_job_start`, and `type_job_end` boolean fields
    * Added the `event_types` array field
* ipam.VLANGroup
    * Removed the `min_vid` and `max_vid` fields
    * Added the `vid_ranges` field, an array of starting & ending VLAN IDs
* virtualization.VirtualMachine
    * Added the optional `serial` field
* wireless.WirelessLink
    * Added the optional `distance` and `distance_unit` fields
