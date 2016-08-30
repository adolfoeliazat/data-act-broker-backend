import factory
from factory import fuzzy

from dataactcore.models import stagingModels


class AppropriationFactory(factory.Factory):
    class Meta:
        model = stagingModels.Appropriation

    appropriation_id = None
    submission_id = fuzzy.FuzzyInteger(9999)
    job_id = fuzzy.FuzzyInteger(9999)
    row_number = fuzzy.FuzzyInteger(1, 9999)
    adjustments_to_unobligated_cpe = fuzzy.FuzzyDecimal(9999)
    agency_identifier = fuzzy.FuzzyText()
    allocation_transfer_agency = fuzzy.FuzzyText()
    availability_type_code = fuzzy.FuzzyText()
    beginning_period_of_availa = fuzzy.FuzzyText()
    borrowing_authority_amount_cpe = fuzzy.FuzzyDecimal(9999)
    budget_authority_appropria_cpe = fuzzy.FuzzyDecimal(9999)
    budget_authority_available_cpe = fuzzy.FuzzyDecimal(9999)
    budget_authority_unobligat_fyb = fuzzy.FuzzyDecimal(9999)
    contract_authority_amount_cpe = fuzzy.FuzzyDecimal(9999)
    deobligations_recoveries_r_cpe = fuzzy.FuzzyDecimal(9999)
    ending_period_of_availabil = fuzzy.FuzzyText()
    gross_outlay_amount_by_tas_cpe = fuzzy.FuzzyDecimal(9999)
    main_account_code = fuzzy.FuzzyText()
    obligations_incurred_total_cpe = fuzzy.FuzzyDecimal(9999)
    other_budgetary_resources_cpe = fuzzy.FuzzyDecimal(9999)
    spending_authority_from_of_cpe = fuzzy.FuzzyDecimal(9999)
    status_of_budgetary_resour_cpe = fuzzy.FuzzyDecimal(9999)
    sub_account_code = fuzzy.FuzzyText()
    unobligated_balance_cpe = fuzzy.FuzzyDecimal(9999)
    tas = fuzzy.FuzzyText()
    is_first_quarter = False


class AwardFinancialFactory(factory.Factory):
    class Meta:
        model = stagingModels.AwardFinancial

    award_financial_id = None
    submission_id = fuzzy.FuzzyInteger(9999)
    job_id = fuzzy.FuzzyInteger(9999)
    row_number = fuzzy.FuzzyInteger(9999)
    agency_identifier = fuzzy.FuzzyText()
    allocation_transfer_agency = fuzzy.FuzzyText()
    availability_type_code = fuzzy.FuzzyText()
    beginning_period_of_availa = fuzzy.FuzzyText()
    by_direct_reimbursable_fun = fuzzy.FuzzyText()
    deobligations_recov_by_awa_cpe = fuzzy.FuzzyDecimal(9999)
    ending_period_of_availabil = fuzzy.FuzzyText()
    fain = fuzzy.FuzzyText()
    gross_outlay_amount_by_awa_cpe = fuzzy.FuzzyDecimal(9999)
    gross_outlay_amount_by_awa_fyb = fuzzy.FuzzyDecimal(9999)
    gross_outlays_delivered_or_cpe = fuzzy.FuzzyDecimal(9999)
    gross_outlays_delivered_or_fyb = fuzzy.FuzzyDecimal(9999)
    gross_outlays_undelivered_cpe = fuzzy.FuzzyDecimal(9999)
    gross_outlays_undelivered_fyb = fuzzy.FuzzyDecimal(9999)
    main_account_code = fuzzy.FuzzyText()
    object_class = fuzzy.FuzzyText()
    obligations_delivered_orde_cpe = fuzzy.FuzzyDecimal(9999)
    obligations_delivered_orde_fyb = fuzzy.FuzzyDecimal(9999)
    obligations_incurred_byawa_cpe = fuzzy.FuzzyDecimal(9999)
    obligations_undelivered_or_cpe = fuzzy.FuzzyDecimal(9999)
    obligations_undelivered_or_fyb = fuzzy.FuzzyDecimal(9999)
    parent_award_id = fuzzy.FuzzyText()
    piid = fuzzy.FuzzyText()
    program_activity_code = fuzzy.FuzzyText()
    program_activity_name = fuzzy.FuzzyText()
    sub_account_code = fuzzy.FuzzyText()
    transaction_obligated_amou = fuzzy.FuzzyDecimal(9999)
    uri = fuzzy.FuzzyText()
    ussgl480100_undelivered_or_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl480100_undelivered_or_fyb = fuzzy.FuzzyDecimal(9999)
    ussgl480200_undelivered_or_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl480200_undelivered_or_fyb = fuzzy.FuzzyDecimal(9999)
    ussgl483100_undelivered_or_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl483200_undelivered_or_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl487100_downward_adjus_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl487200_downward_adjus_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl488100_upward_adjustm_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl488200_upward_adjustm_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl490100_delivered_orde_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl490100_delivered_orde_fyb = fuzzy.FuzzyDecimal(9999)
    ussgl490200_delivered_orde_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl490800_authority_outl_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl490800_authority_outl_fyb = fuzzy.FuzzyDecimal(9999)
    ussgl493100_delivered_orde_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl497100_downward_adjus_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl497200_downward_adjus_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl498100_upward_adjustm_cpe = fuzzy.FuzzyDecimal(9999)
    ussgl498200_upward_adjustm_cpe = fuzzy.FuzzyDecimal(9999)
    tas = fuzzy.FuzzyText()
    is_first_quarter = False
