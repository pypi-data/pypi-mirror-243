from functools import singledispatch, singledispatchmethod
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, Retry

media_type = dict(json="application/json", xml="text/xml", nh="text/x-nh", phyloxml="text/x-phyloxml+xml",
                  orthoxml="text/x-orthoxml+xml", gff3="text/x-gff3", fasta="text/x-fasta", bed="text/x-bed",
                  seqxml="text/x-seqxml+xml", text="text/plain", yaml="text/x-yaml", jsonp="text/javascript", )

server = "http://grch37.rest.ensembl.org"
session = requests.Session()
adapter = HTTPAdapter(
    max_retries=Retry(backoff_factor=3600 / 55000, respect_retry_after_header=True, status_forcelist=[429],
                      allowed_methods=["GET", "POST"], ))
session.mount(server, adapter)


def get(endpoint, params, response_format):
    headers = {"Content-Type": media_type[response_format]}
    response = session.get(urljoin(server, endpoint), headers=headers, params=params)
    if response.ok:
        if headers["Content-Type"] == "application/json":
            return response.json()
        else:
            return response.text
    else:
        response.raise_for_status()


def post(endpoint, params, json, response_format):
    headers = {"Content-Type": media_type[response_format], "Accept": media_type[response_format]}
    response = session.post(urljoin(server, endpoint), headers=headers, params=params, json=json)
    if response.ok:
        if headers["Accept"] == "application/json":
            return response.json()
        else:
            return response.text
    else:
        response.raise_for_status()


@singledispatch
def archive(id: str, callback=None, response_format="json"):
    return get(f"archive/id/{id}", params=dict(callback=callback), response_format=response_format, )


@archive.register
def _(id: list, callback=None, response_format="json"):
    return post(f"archive/id", params=dict(callback=callback), response_format=response_format, json=dict(id=id), )


def genomic_alignment_region(region: str, species: str, aligned=None, callback=None, mask=None, method=None,
                             response_format="json", ):
    return get(f"alignment/region/{species}/{region}",
               params=dict(aligned=aligned, callback=callback, mask=mask, method=method),
               response_format=response_format, )


def homology_ensemblgene(id: str, aligned=None, callback=None, cigar_line=None, format=None, sequence=None, type=None,
                         response_format="json", ):
    return get(f"homology/id/{id}",
               params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, format=format, sequence=sequence,
                           type=type, ), response_format=response_format, )


def homology_species_gene_id(id: str, species: str, aligned=None, callback=None, cigar_line=None, format=None,
                             sequence=None, type=None, response_format="json", ):
    return get(f"homology/id/{species}/{id}",
               params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, format=format, sequence=sequence,
                           type=type, ), response_format=response_format, )


def homology_symbol(species: str, symbol: str, aligned=None, callback=None, cigar_line=None, external_db=None,
                    format=None, sequence=None, type=None, response_format="json", ):
    return get(f"homology/symbol/{species}/{symbol}",
               params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, external_db=external_db,
                           format=format, sequence=sequence, type=type, ), response_format=response_format, )


def xref_external(species: str, symbol: str, callback=None, db_type=None, external_db=None, object_type=None,
                  response_format="json", ):
    return get(f"xrefs/symbol/{species}/{symbol}",
               params=dict(callback=callback, db_type=db_type, external_db=external_db, object_type=object_type, ),
               response_format=response_format, )


def xref_id(id: str, all_levels=None, callback=None, db_type=None, external_db=None, object_type=None, species=None,
            response_format="json", ):
    return get(f"xrefs/id/{id}",
               params=dict(all_levels=all_levels, callback=callback, db_type=db_type, external_db=external_db,
                           object_type=object_type, species=species, ), response_format=response_format, )


def xref_name(name: str, species: str, callback=None, db_type=None, external_db=None, response_format="json", ):
    return get(f"xrefs/name/{species}/{name}", params=dict(callback=callback, db_type=db_type, external_db=external_db),
               response_format=response_format, )


def analysis(species: str, callback=None, response_format="json"):
    return get(f"info/analysis/{species}", params=dict(callback=callback), response_format=response_format, )


def assembly_info(species: str, bands=None, callback=None, synonyms=None, response_format="json"):
    return get(f"info/assembly/{species}", params=dict(bands=bands, callback=callback, synonyms=synonyms),
               response_format=response_format, )


def assembly_stats(region_name: str, species: str, bands=None, callback=None, synonyms=None, response_format="json", ):
    return get(f"info/assembly/{species}/{region_name}", params=dict(bands=bands, callback=callback, synonyms=synonyms),
               response_format=response_format, )


def biotypes(species: str, callback=None, response_format="json"):
    return get(f"info/biotypes/{species}", params=dict(callback=callback), response_format=response_format, )


def biotypes_groups(callback=None, group=None, object_type=None, response_format="json"):
    return get(f"info/biotypes/groups/{group}/{object_type}",
               params=dict(callback=callback, group=group, object_type=object_type), response_format=response_format, )


def biotypes_name(name: str, callback=None, object_type=None, response_format="json"):
    return get(f"info/biotypes/name/{name}/{object_type}", params=dict(callback=callback, object_type=object_type),
               response_format=response_format, )


def compara_methods(callback=None, compara=None, response_format="json", **kwargs):
    return get(f"info/compara/methods", params=dict(callback=callback, compara=compara, **kwargs),
               response_format=response_format, )


def compara_species_sets(method: str, callback=None, compara=None, response_format="json"):
    return get(f"info/compara/species_sets/{method}", params=dict(callback=callback, compara=compara),
               response_format=response_format, )


def comparas(callback=None, response_format="json"):
    return get(f"info/comparas", params=dict(callback=callback), response_format=response_format, )


def data(callback=None, response_format="json"):
    return get(f"info/data", params=dict(callback=callback), response_format=response_format)


def external_dbs(species: str, callback=None, feature=None, filter=None, response_format="json"):
    return get(f"info/external_dbs/{species}", params=dict(callback=callback, feature=feature, filter=filter),
               response_format=response_format, )


def ping(callback=None, response_format="json"):
    return get(f"info/ping", params=dict(callback=callback), response_format=response_format)


def rest(callback=None, response_format="json"):
    return get(f"info/rest", params=dict(callback=callback), response_format=response_format)


def software(callback=None, response_format="json"):
    return get(f"info/software", params=dict(callback=callback), response_format=response_format, )


def species(callback=None, division=None, hide_strain_info=None, strain_collection=None, response_format="json", ):
    return get(f"info/species", params=dict(callback=callback, division=division, hide_strain_info=hide_strain_info,
                                            strain_collection=strain_collection, ), response_format=response_format, )


def variation(species: str, callback=None, filter=None, response_format="json"):
    return get(f"info/variation/{species}", params=dict(callback=callback, filter=filter),
               response_format=response_format, )


def variation_consequence_types(callback=None, rank=None, response_format="json"):
    return get(f"info/variation/consequence_types", params=dict(callback=callback, rank=rank),
               response_format=response_format, )


def variation_population_name(population_name: str, species: str, callback=None, response_format="json"):
    return get(f"info/variation/populations/{species}/{population_name}", params=dict(callback=callback),
               response_format=response_format, )


def variation_populations(species: str, callback=None, filter=None, response_format="json"):
    return get(f"info/variation/populations/{species}", params=dict(callback=callback, filter=filter),
               response_format=response_format, )


def ld_id_get(id: str, population_name: str, species: str, attribs=None, callback=None, d_prime=None, r2=None,
              window_size=None, response_format="json", ):
    return get(f"ld/{species}/{id}/{population_name}",
               params=dict(attribs=attribs, callback=callback, d_prime=d_prime, r2=r2, window_size=window_size, ),
               response_format=response_format, )


def ld_pairwise_get(id1: str, id2: str, species: str, callback=None, d_prime=None, population_name=None, r2=None,
                    response_format="json", ):
    return get(f"ld/{species}/pairwise/{id1}/{id2}",
               params=dict(callback=callback, d_prime=d_prime, population_name=population_name, r2=r2),
               response_format=response_format, )


def ld_region_get(population_name: str, region: str, species: str, callback=None, d_prime=None, r2=None,
                  response_format="json", ):
    return get(f"ld/{species}/region/{region}/{population_name}",
               params=dict(callback=callback, d_prime=d_prime, r2=r2), response_format=response_format, )


@singledispatch
def lookup(id: str, callback=None, db_type=None, expand=None, format=None, mane=None, phenotypes=None, species=None,
           utr=None, response_format="json", ):
    return get(f"lookup/id/{id}",
               params=dict(callback=callback, db_type=db_type, expand=expand, format=format, mane=mane,
                           phenotypes=phenotypes, species=species, utr=utr, ), response_format=response_format, )


@lookup.register
def _(id: list, callback=None, db_type=None, expand=None, format=None, object_type=None, species=None,
      response_format="json", ):
    return post(f"lookup/id",
                params=dict(callback=callback, db_type=db_type, expand=expand, format=format, object_type=object_type,
                            species=species, ), response_format=response_format, json={"ids": id}, )


@singledispatch
def symbol_lookup(symbol: str, species: str, callback=None, expand=None, format=None, response_format="json", ):
    return get(f"lookup/symbol/{species}/{symbol}", params=dict(callback=callback, expand=expand, format=format),
               response_format=response_format, )


@symbol_lookup.register
def _(symbol: list, species: str, callback=None, expand=None, format=None, response_format="json", ):
    return post(f"lookup/symbol/{species}/{symbol}", params=dict(callback=callback, expand=expand, format=format),
                response_format=response_format, json={"symbols": symbol}, )


def assembly_cdna(id: str, region: str, callback=None, include_original_region=None, species=None,
                  response_format="json", ):
    return get(f"map/cdna/{id}/{region}",
               params=dict(callback=callback, include_original_region=include_original_region, species=species, ),
               response_format=response_format, )


def assembly_cds(id: str, region: str, callback=None, include_original_region=None, species=None,
                 response_format="json", ):
    return get(f"map/cds/{id}/{region}",
               params=dict(callback=callback, include_original_region=include_original_region, species=species, ),
               response_format=response_format, )


def assembly_map(asm_one: str, asm_two: str, region: str, species: str, callback=None, coord_system=None,
                 target_coord_system=None, response_format="json", ):
    return get(f"map/{species}/{asm_one}/{region}/{asm_two}",
               params=dict(callback=callback, coord_system=coord_system, target_coord_system=target_coord_system, ),
               response_format=response_format, )


def assembly_translation(id: str, region: str, callback=None, species=None, response_format="json"):
    return get(f"map/translation/{id}/{region}", params=dict(callback=callback, species=species),
               response_format=response_format, )


def ontology_ancestors(id: str, callback=None, ontology=None, response_format="json"):
    return get(f"ontology/ancestors/{id}", params=dict(callback=callback, ontology=ontology),
               response_format=response_format, )


def ontology_ancestors_chart(id: str, callback=None, ontology=None, response_format="json"):
    return get(f"ontology/ancestors/chart/{id}", params=dict(callback=callback, ontology=ontology),
               response_format=response_format, )


def ontology_descendants(id: str, callback=None, closest_term=None, ontology=None, subset=None, zero_distance=None,
                         response_format="json", ):
    return get(f"ontology/descendants/{id}",
               params=dict(callback=callback, closest_term=closest_term, ontology=ontology, subset=subset,
                           zero_distance=zero_distance, ), response_format=response_format, )


def ontology_id(id: str, callback=None, relation=None, simple=None, response_format="json"):
    return get(f"ontology/id/{id}", params=dict(callback=callback, relation=relation, simple=simple),
               response_format=response_format, )


def ontology_name(name: str, callback=None, ontology=None, relation=None, simple=None, response_format="json", ):
    return get(f"ontology/name/{name}",
               params=dict(callback=callback, ontology=ontology, relation=relation, simple=simple),
               response_format=response_format, )


def taxonomy_classification(id: str, callback=None, response_format="json"):
    return get(f"taxonomy/classification/{id}", params=dict(callback=callback), response_format=response_format, )


def taxonomy_id(id: str, callback=None, simple=None, response_format="json"):
    return get(f"taxonomy/id/{id}", params=dict(callback=callback, simple=simple), response_format=response_format, )


def taxonomy_name(name: str, callback=None, response_format="json"):
    return get(f"taxonomy/name/{name}", params=dict(callback=callback), response_format=response_format, )


def overlap_id(id: str, feature: str, biotype=None, callback=None, db_type=None, logic_name=None, misc_set=None,
               object_type=None, so_term=None, species=None, species_set=None, variant_set=None,
               response_format="json", ):
    return get(f"overlap/id/{id}",
               params=dict(feature=feature, biotype=biotype, callback=callback, db_type=db_type, logic_name=logic_name,
                           misc_set=misc_set, object_type=object_type, so_term=so_term, species=species,
                           species_set=species_set, variant_set=variant_set, ), response_format=response_format, )


def overlap_region(region: str, feature: str, species: str, biotype=None, callback=None, db_type=None, logic_name=None,
                   misc_set=None, so_term=None, species_set=None, trim_downstream=None, trim_upstream=None,
                   variant_set=None, response_format="json", ):
    return get(f"overlap/region/{species}/{region}",
               params=dict(feature=feature, biotype=biotype, callback=callback, db_type=db_type, logic_name=logic_name,
                           misc_set=misc_set, so_term=so_term, species_set=species_set, trim_downstream=trim_downstream,
                           trim_upstream=trim_upstream, variant_set=variant_set, ), response_format=response_format, )


def overlap_translation(id: str, callback=None, db_type=None, feature=None, so_term=None, species=None, type=None,
                        response_format="json", ):
    return get(f"overlap/translation/{id}",
               params=dict(callback=callback, db_type=db_type, feature=feature, so_term=so_term, species=species,
                           type=type, ), response_format=response_format, )


def phenotype_accession(accession: str, species: str, callback=None, include_children=None, include_pubmed_id=None,
                        include_review_status=None, source=None, response_format="json", ):
    return get(f"/phenotype/accession/{species}/{accession}",
               params=dict(callback=callback, include_children=include_children, include_pubmed_id=include_pubmed_id,
                           include_review_status=include_review_status, source=source, ),
               response_format=response_format, )


def phenotype_gene(gene: str, species: str, callback=None, include_associated=None, include_overlap=None,
                   include_pubmed_id=None, include_review_status=None, include_submitter=None, non_specified=None,
                   trait=None, tumour=None, response_format="json", ):
    return get(f"/phenotype/gene/{species}/{gene}",
               params=dict(callback=callback, include_associated=include_associated, include_overlap=include_overlap,
                           include_pubmed_id=include_pubmed_id, include_review_status=include_review_status,
                           include_submitter=include_submitter, non_specified=non_specified, trait=trait,
                           tumour=tumour, ), response_format=response_format, )


def phenotype_region(region: str, species: str, callback=None, feature_type=None, include_pubmed_id=None,
                     include_review_status=None, include_submitter=None, non_specified=None, only_phenotypes=None,
                     trait=None, tumour=None, response_format="json", ):
    return get(f"/phenotype/region/{species}/{region}",
               params=dict(callback=callback, feature_type=feature_type, include_pubmed_id=include_pubmed_id,
                           include_review_status=include_review_status, include_submitter=include_submitter,
                           non_specified=non_specified, only_phenotypes=only_phenotypes, trait=trait, tumour=tumour, ),
               response_format=response_format, )


def phenotype_term(species: str, term: str, callback=None, include_children=None, include_pubmed_id=None,
                   include_review_status=None, source=None, response_format="json", ):
    return get(f"/phenotype/term/{species}/{term}",
               params=dict(callback=callback, include_children=include_children, include_pubmed_id=include_pubmed_id,
                           include_review_status=include_review_status, source=source, ),
               response_format=response_format, )


def array(microarray: str, species: str, vendor: str, callback=None, response_format="json"):
    return get(f"regulatory/species/{species}/microarray/{microarray}/vendor/{vendor}", params=dict(callback=callback),
               response_format=response_format, )


def fetch_all_epigenomes(species: str, callback=None, response_format="json"):
    return get(f"regulatory/species/{species}/epigenome", params=dict(callback=callback),
               response_format=response_format, )


def get_binding_matrix(binding_matrix: str, species: str, callback=None, unit=None, response_format="json"):
    return get(f"species/{species}/binding_matrix/{binding_matrix}/", params=dict(callback=callback, unit=unit),
               response_format=response_format, )


def list_all_microarrays(species: str, callback=None, response_format="json"):
    return get(f"regulatory/species/{species}/microarray", params=dict(callback=callback),
               response_format=response_format, )


def probe(microarray: str, probe: str, species: str, callback=None, gene=None, transcripts=None,
          response_format="json", ):
    return get(f"regulatory/species/{species}/microarray/{microarray}/probe/{probe}",
               params=dict(callback=callback, gene=gene, transcripts=transcripts), response_format=response_format, )


def probe_set(microarray: str, probe_set: str, species: str, callback=None, gene=None, transcripts=None,
              response_format="json", ):
    return get(f"regulatory/species/{species}/microarray/{microarray}/probe_set/{probe_set}",
               params=dict(callback=callback, gene=gene, transcripts=transcripts), response_format=response_format, )


def regulatory_id(id: str, species: str, activity=None, callback=None, response_format="json"):
    return get(f"regulatory/species/{species}/id/{id}", params=dict(activity=activity, callback=callback),
               response_format=response_format, )


@singledispatch
def sequence_id(id: str, callback=None, db_type=None, end=None, expand_3prime=None, expand_5prime=None, format=None,
                mask=None, mask_feature=None, multiple_sequences=None, object_type=None, species=None, start=None,
                type=None, response_format="json", ):
    return get(f"sequence/id/{id}",
               params=dict(callback=callback, db_type=db_type, end=end, expand_3prime=expand_3prime,
                           expand_5prime=expand_5prime, format=format, mask=mask, mask_feature=mask_feature,
                           multiple_sequences=multiple_sequences, object_type=object_type, species=species, start=start,
                           type=type, ), response_format=response_format, )


@sequence_id.register
def _(id: list, callback=None, db_type=None, end=None, expand_3prime=None, expand_5prime=None, format=None, mask=None,
      mask_feature=None, object_type=None, species=None, start=None, type=None, response_format="json", ):
    return post(f"sequence/id", params=dict(callback=callback, db_type=db_type, end=end, expand_3prime=expand_3prime,
                                            expand_5prime=expand_5prime, format=format, mask=mask,
                                            mask_feature=mask_feature, object_type=object_type, species=species,
                                            start=start, type=type, ), response_format=response_format,
                json={"ids": id}, )


@singledispatch
def sequence_region(region: str, species: str, callback=None, coord_system=None, coord_system_version=None,
                    expand_3prime=None, expand_5prime=None, format=None, mask=None, mask_feature=None,
                    response_format="json", ):
    return get(f"sequence/region/{species}/{region}",
               params=dict(callback=callback, coord_system=coord_system, coord_system_version=coord_system_version,
                           expand_3prime=expand_3prime, expand_5prime=expand_5prime, format=format, mask=mask,
                           mask_feature=mask_feature, ), response_format=response_format, )


@sequence_region.register
def _(region: list, species: str, callback=None, coord_system=None, coord_system_version=None, expand_3prime=None,
      expand_5prime=None, format=None, mask=None, mask_feature=None, response_format="json", ):
    return post(f"sequence/region/{species}",
                params=dict(callback=callback, coord_system=coord_system, coord_system_version=coord_system_version,
                            expand_3prime=expand_3prime, expand_5prime=expand_5prime, format=format, mask=mask,
                            mask_feature=mask_feature, ), response_format=response_format, json={"regions": region}, )


def transcript_haplotypes_get(id: str, species: str, aligned_sequences=None, callback=None, samples=None, sequence=None,
                              response_format="json", ):
    return get(f"transcript_haplotypes/{species}/{id}",
               params=dict(aligned_sequences=aligned_sequences, callback=callback, samples=samples,
                           sequence=sequence, ), response_format=response_format, )


@singledispatch
def vep_hgvs(hgvs_notation: str, species: str, AncestralAllele=None, Blosum62=None, CADD=None, Conservation=None,
             DisGeNET=None, EVE=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None,
             MaveDB=None, MaxEntScan=None, NMD=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None,
             ambiguous_hgvs=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None,
             distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
             flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None,
             minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
             pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
             transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
             xref_refseq=None, response_format="json", ):
    return get(f"vep/{species}/hgvs/{hgvs_notation}",
               params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, Conservation=Conservation,
                           DisGeNET=DisGeNET, EVE=EVE, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                           LoF=LoF, Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                           Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                           ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback, canonical=canonical,
                           ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance, domains=domains, failed=failed,
                           flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                           flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                           gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                           mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                           pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                           protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                           transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                           variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq, ),
               response_format=response_format, )


@vep_hgvs.register
def _(hgvs_notation: list, species: str, AncestralAllele=None, Blosum62=None, CADD=None, DisGeNET=None, EVE=None,
      GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None,
      NMD=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None, appris=None, callback=None,
      canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None,
      flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None,
      merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
      pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
      transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
      xref_refseq=None, response_format="json", ):
    return post(f"vep/{species}/hgvs",
                params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, DisGeNET=DisGeNET, EVE=EVE,
                            GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                            Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, Phenotypes=Phenotypes,
                            SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, ambiguous_hgvs=ambiguous_hgvs, appris=appris,
                            callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                            distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                            flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                            ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged,
                            minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene,
                            pick=pick, pick_allele=pick_allele, pick_allele_gene=pick_allele_gene,
                            pick_order=pick_order, protein=protein, refseq=refseq, shift_3prime=shift_3prime,
                            shift_genomic=shift_genomic, transcript_id=transcript_id,
                            transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                            variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq, ),
                response_format=response_format, json={"hgvs_notations": hgvs_notation}, )


@singledispatch
def vep_id(id: str, species: str, AncestralAllele=None, Blosum62=None, CADD=None, Conservation=None, DisGeNET=None,
           EVE=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None,
           MaxEntScan=None, NMD=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None,
           canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None,
           flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None,
           hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None,
           pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None,
           shift_3prime=None, shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
           variant_class=None, vcf_string=None, xref_refseq=None, response_format="json", ):
    return get(f"vep/{species}/id/{id}",
               params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, Conservation=Conservation,
                           DisGeNET=DisGeNET, EVE=EVE, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                           LoF=LoF, Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                           Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris,
                           callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                           distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                           flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                           ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged,
                           minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                           pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                           protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                           transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                           variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq, ),
               response_format=response_format, )


@vep_id.register
def _(id: list, species: str, AncestralAllele=None, Blosum62=None, CADD=None, DisGeNET=None, EVE=None, GO=None,
      GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None,
      Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None,
      dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
      flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None,
      mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None,
      pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
      transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
      response_format="json", ):
    return post(f"vep/{species}/id",
                params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, DisGeNET=DisGeNET, EVE=EVE,
                            GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                            Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, Phenotypes=Phenotypes,
                            SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris, callback=callback,
                            canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance,
                            domains=domains, failed=failed, flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                            flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                            gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                            mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                            pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                            protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                            transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                            uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                            xref_refseq=xref_refseq, ), response_format=response_format, json={"ids": id}, )


@singledispatch
def vep_region(region: str, allele: str, species: str, AncestralAllele=None, Blosum62=None, CADD=None,
               Conservation=None, DisGeNET=None, EVE=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None,
               LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, Phenotypes=None, SpliceAI=None,
               UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None,
               distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
               flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None,
               minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
               pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
               transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
               xref_refseq=None, response_format="json", ):
    return get(f"vep/{species}/region/{region}/{allele}/",
               params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, Conservation=Conservation,
                           DisGeNET=DisGeNET, EVE=EVE, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct,
                           LoF=LoF, Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                           Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris,
                           callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                           distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                           flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                           ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged,
                           minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                           pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                           protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                           transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl, uniprot=uniprot,
                           variant_class=variant_class, vcf_string=vcf_string, xref_refseq=xref_refseq, ),
               response_format=response_format, )


@vep_region.register
def _(region: list, species: str, AncestralAllele=None, Blosum62=None, CADD=None, DisGeNET=None, EVE=None, GO=None,
      GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None,
      Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None,
      dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
      flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None,
      mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None,
      pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
      transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
      response_format="json", ):
    return post(f"vep/{species}/region",
                params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, DisGeNET=DisGeNET, EVE=EVE,
                            GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                            Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD, Phenotypes=Phenotypes,
                            SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris, callback=callback,
                            canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance,
                            domains=domains, failed=failed, flag_pick=flag_pick, flag_pick_allele=flag_pick_allele,
                            flag_pick_allele_gene=flag_pick_allele_gene, ga4gh_vrs=ga4gh_vrs,
                            gencode_basic=gencode_basic, hgvs=hgvs, mane=mane, merged=merged, minimal=minimal,
                            mirna=mirna, mutfunc=mutfunc, numbers=numbers, per_gene=per_gene, pick=pick,
                            pick_allele=pick_allele, pick_allele_gene=pick_allele_gene, pick_order=pick_order,
                            protein=protein, refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                            transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                            uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                            xref_refseq=xref_refseq, ), response_format=response_format, json={"variants": region}, )


@singledispatch
def variant_recoder(id: str, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None,
                    minimal=None, var_synonyms=None, vcf_string=None, response_format="json", ):
    return get(f"variant_recoder/{species}/{id}",
               params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                           gencode_basic=gencode_basic, minimal=minimal, var_synonyms=var_synonyms,
                           vcf_string=vcf_string, ), response_format=response_format, )


@variant_recoder.register
def _(id: list, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None, minimal=None,
      var_synonyms=None, vcf_string=None, response_format="json", ):
    return post(f"variant_recoder/{species}",
                params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                            gencode_basic=gencode_basic, minimal=minimal, var_synonyms=var_synonyms,
                            vcf_string=vcf_string, ), response_format=response_format, json={"ids": id}, )


@singledispatch
def variation_id(id: str, species: str, callback=None, genotypes=None, genotyping_chips=None, phenotypes=None,
                 pops=None, population_genotypes=None, response_format="json", ):
    return get(f"variation/{species}/{id}",
               params=dict(callback=callback, genotypes=genotypes, genotyping_chips=genotyping_chips,
                           phenotypes=phenotypes, pops=pops, population_genotypes=population_genotypes, ),
               response_format=response_format, )


@variation_id.register
def _(id: list, species: str, callback=None, genotypes=None, phenotypes=None, pops=None, population_genotypes=None,
      response_format="json", ):
    return post(f"variation/{species}/",
                params=dict(callback=callback, genotypes=genotypes, phenotypes=phenotypes, pops=pops,
                            population_genotypes=population_genotypes, ), response_format=response_format,
                json={"ids": id}, )


def variation_pmcid_get(pmcid: str, species: str, callback=None, response_format="json"):
    return get(f"variation/{species}/pmcid/{pmcid}", params=dict(callback=callback), response_format=response_format, )


def variation_pmid_get(pmid: str, species: str, callback=None, response_format="json"):
    return get(f"variation/{species}/pmid/{pmid}", params=dict(callback=callback), response_format=response_format, )


def beacon_get(callback=None, response_format="json"):
    return get(f"ga4gh/beacon", params=dict(callback=callback), response_format=response_format)


def beacon_query_get(response_format="json", **kwargs, ):
    return get(f"ga4gh/beacon/query", params=dict(**kwargs), response_format=response_format)


def beacon_query_post(response_format="json", **kwargs):
    return post(f"ga4gh/beacon/query", params={}, response_format=response_format, json=dict(**kwargs))


def features_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/features/{id}", params=dict(callback=callback), response_format=response_format)


def features_post(response_format="json", **kwargs):
    return post(f"ga4gh/features/search", params={}, response_format=response_format, json=dict(**kwargs))


def gacallSet(response_format="json", **kwargs):
    return post(f"ga4gh/callsets/search", params={}, response_format=response_format, json=dict(**kwargs))


def gacallset_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/callsets/{id}", params=dict(callback=callback), response_format=response_format)


def gadataset(callback=None, pageSize=None, pageToken=None, response_format="json"):
    return post(f"ga4gh/datasets/search", params=dict(callback=callback),
                json=dict(pageSize=pageSize, pageToken=pageToken), response_format=response_format, )


def gadataset_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/datasets/{id}", params=dict(callback=callback), response_format=response_format, )


def gafeatureset(datasetId: str, callback=None, pageSize=None, pageToken=None, response_format="json"):
    return post(f"ga4gh/featuresets/search", params=dict(callback=callback),
                json=dict(datasetId=datasetId, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format, )


def gafeatureset_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/featuresets/{id}", params=dict(callback=callback), response_format=response_format, )


def gavariant_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/variants/{id}", params=dict(callback=callback), response_format=response_format, )


def gavariantannotations(variantAnnotationSetId: str, callback=None, effects=None, end=None, pageSize=None,
                         pageToken=None, referenceId=None, referenceName=None, start=None, response_format="json", ):
    return post(f"ga4gh/variantannotations/search", params=dict(callback=callback),
                json=dict(variantAnnotationSetId=variantAnnotationSetId, effects=effects, end=end, pageSize=pageSize,
                          pageToken=pageToken, referenceId=referenceId, referenceName=referenceName, start=start, ),
                response_format=response_format, )


def gavariants(end: str, referenceName: str, start: str, variantSetId: str, callSetIds=None, callback=None,
               pageSize=None, pageToken=None, response_format="json", ):
    return post(f"ga4gh/variants/search", params=dict(callback=callback),
                json=dict(pageSize=pageSize, pageToken=pageToken, callSetIds=callSetIds, end=end,
                          referenceName=referenceName, start=start, variantSetId=variantSetId, ),
                response_format=response_format, )


def gavariantset(datasetId: str, callback=None, pageSize=None, pageToken=None, response_format="json"):
    return post(f"ga4gh/variantsets/search", params=dict(callback=callback),
                json=dict(datasetId=datasetId, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format, )


def gavariantset_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/variantsets/{id}", params=dict(callback=callback), response_format=response_format, )


def references(referenceSetId: str, accession=None, callback=None, md5checksum=None, pageSize=None, pageToken=None,
               response_format="json", ):
    return post(f"ga4gh/references/search", params=dict(callback=callback),
                json=dict(accession=accession, referenceSetId=referenceSetId, md5checksum=md5checksum,
                          pageSize=pageSize, pageToken=pageToken, ), response_format=response_format, )


def references_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/references/{id}", params=dict(callback=callback), response_format=response_format, )


def referenceSets(accession=None, callback=None, pageSize=None, pageToken=None, response_format="json"):
    return post(f"ga4gh/referencesets/search", params=dict(

        callback=callback), json=dict(accession=accession, pageSize=pageSize, pageToken=pageToken, ),
                response_format=response_format, )


def referenceSets_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/referencesets/{id}", params=dict(callback=callback), response_format=response_format, )


def VariantAnnotationSet(variantSetId: str, callback=None, pageSize=None, pageToken=None, response_format="json", ):
    return post(f"ga4gh/variantannotationsets/search", params=dict(callback=callback),
                json=dict(variantSetId=variantSetId, pageSize=pageSize, pageToken=pageToken),
                response_format=response_format, )


def VariantAnnotationSet_id(id: str, callback=None, response_format="json"):
    return get(f"ga4gh/variantannotationsets/{id}", params=dict(callback=callback), response_format=response_format, )


class Ensembl:
    def __init__(self):
        self.server = "http://grch37.rest.ensembl.org"
        self.session = requests.Session()
        self.adapter = HTTPAdapter(
            max_retries=Retry(backoff_factor=3600 / 55000, respect_retry_after_header=True, status_forcelist=[429],
                              allowed_methods=["GET", "POST"], ))
        self.session.mount(self.server, self.adapter)

    def get(self, endpoint, params, response_format):
        headers = {}
        headers["Content-Type"] = media_type[response_format]
        response = self.session.get(urljoin(self.server, endpoint), headers=headers, params=params)
        if response.ok:
            if headers["Content-Type"] == "application/json":
                return response.json()
            else:
                return response.text
        else:
            response.raise_for_status()

    def post(self, endpoint, params, json, response_format):
        headers = {}
        headers["Content-Type"] = media_type[response_format]
        headers["Accept"] = media_type[response_format]
        response = self.session.post(urljoin(self.server, endpoint), headers=headers, params=params, json=json)
        if response.ok:
            if headers["Accept"] == "application/json":
                return response.json()
            else:
                return response.text
        else:
            response.raise_for_status()

    @singledispatchmethod
    def archive(self, id: str, callback=None, response_format="json"):
        return self.get(f"archive/id/{id}", params=dict(callback=callback), response_format=response_format, )

    @archive.register
    def _(self, id: list, callback=None, response_format="json"):
        return self.post(f"archive/id", params=dict(callback=callback), response_format=response_format,
                         json=dict(id=id), )

    def genomic_alignment_region(self, region: str, species: str, aligned=None, callback=None, mask=None, method=None,
                                 response_format="json", ):
        return self.get(f"alignment/region/{species}/{region}",
                        params=dict(aligned=aligned, callback=callback, mask=mask, method=method),
                        response_format=response_format, )

    def homology_ensemblgene(self, id: str, aligned=None, callback=None, cigar_line=None, format=None, sequence=None,
                             type=None, response_format="json", ):
        return self.get(f"homology/id/{id}",
                        params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, format=format,
                                    sequence=sequence, type=type, ), response_format=response_format, )

    def homology_species_gene_id(self, id: str, species: str, aligned=None, callback=None, cigar_line=None, format=None,
                                 sequence=None, type=None, response_format="json", ):
        return self.get(f"homology/id/{species}/{id}",
                        params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, format=format,
                                    sequence=sequence, type=type, ), response_format=response_format, )

    def homology_symbol(self, species: str, symbol: str, aligned=None, callback=None, cigar_line=None, external_db=None,
                        format=None, sequence=None, type=None, response_format="json", ):
        return self.get(f"homology/symbol/{species}/{symbol}",
                        params=dict(aligned=aligned, callback=callback, cigar_line=cigar_line, external_db=external_db,
                                    format=format, sequence=sequence, type=type, ), response_format=response_format, )

    def xref_external(self, species: str, symbol: str, callback=None, db_type=None, external_db=None, object_type=None,
                      response_format="json", ):
        return self.get(f"xrefs/symbol/{species}/{symbol}",
                        params=dict(callback=callback, db_type=db_type, external_db=external_db,
                                    object_type=object_type, ), response_format=response_format, )

    def xref_id(self, id: str, all_levels=None, callback=None, db_type=None, external_db=None, object_type=None,
                species=None, response_format="json", ):
        return self.get(f"xrefs/id/{id}",
                        params=dict(all_levels=all_levels, callback=callback, db_type=db_type, external_db=external_db,
                                    object_type=object_type, species=species, ), response_format=response_format, )

    def xref_name(self, name: str, species: str, callback=None, db_type=None, external_db=None,
                  response_format="json", ):
        return self.get(f"xrefs/name/{species}/{name}",
                        params=dict(callback=callback, db_type=db_type, external_db=external_db),
                        response_format=response_format, )

    def analysis(self, species: str, callback=None, response_format="json"):
        return self.get(f"info/analysis/{species}", params=dict(callback=callback), response_format=response_format, )

    def assembly_info(self, species: str, bands=None, callback=None, synonyms=None, response_format="json", ):
        return self.get(f"info/assembly/{species}", params=dict(bands=bands, callback=callback, synonyms=synonyms),
                        response_format=response_format, )

    def assembly_stats(self, region_name: str, species: str, bands=None, callback=None, synonyms=None,
                       response_format="json", ):
        return self.get(f"info/assembly/{species}/{region_name}",
                        params=dict(bands=bands, callback=callback, synonyms=synonyms),
                        response_format=response_format, )

    def biotypes(self, species: str, callback=None, response_format="json"):
        return self.get(f"info/biotypes/{species}", params=dict(callback=callback), response_format=response_format, )

    def biotypes_groups(self, callback=None, group=None, object_type=None, response_format="json"):
        return self.get(f"info/biotypes/groups/{group}/{object_type}",
                        params=dict(callback=callback, group=group, object_type=object_type),
                        response_format=response_format, )

    def biotypes_name(self, name: str, callback=None, object_type=None, response_format="json"):
        return self.get(f"info/biotypes/name/{name}/{object_type}",
                        params=dict(callback=callback, object_type=object_type), response_format=response_format, )

    def compara_methods(self, callback=None, compara=None, response_format="json", **kwargs):
        return self.get(f"info/compara/methods", params=dict(callback=callback, compara=compara, **kwargs),
                        response_format=response_format, )

    def compara_species_sets(self, method: str, callback=None, compara=None, response_format="json"):
        return self.get(f"info/compara/species_sets/{method}", params=dict(callback=callback, compara=compara),
                        response_format=response_format, )

    def comparas(self, callback=None, response_format="json"):
        return self.get(f"info/comparas", params=dict(callback=callback), response_format=response_format, )

    def data(self, callback=None, response_format="json"):
        return self.get(f"info/data", params=dict(callback=callback), response_format=response_format, )

    def external_dbs(self, species: str, callback=None, feature=None, filter=None, response_format="json", ):
        return self.get(f"info/external_dbs/{species}", params=dict(callback=callback, feature=feature, filter=filter),
                        response_format=response_format, )

    def ping(self, callback=None, response_format="json"):
        return self.get(f"info/ping", params=dict(callback=callback), response_format=response_format, )

    def rest(self, callback=None, response_format="json"):
        return self.get(f"info/rest", params=dict(callback=callback), response_format=response_format)

    def software(self, callback=None, response_format="json"):
        return self.get(f"info/software", params=dict(callback=callback), response_format=response_format, )

    def species(self, callback=None, division=None, hide_strain_info=None, strain_collection=None,
                response_format="json", ):
        return self.get(f"info/species",
                        params=dict(callback=callback, division=division, hide_strain_info=hide_strain_info,
                                    strain_collection=strain_collection, ), response_format=response_format, )

    def variation(self, species: str, callback=None, filter=None, response_format="json"):
        return self.get(f"info/variation/{species}", params=dict(callback=callback, filter=filter),
                        response_format=response_format, )

    def variation_consequence_types(self, callback=None, rank=None, response_format="json"):
        return self.get(f"info/variation/consequence_types", params=dict(callback=callback, rank=rank),
                        response_format=response_format, )

    def variation_population_name(self, population_name: str, species: str, callback=None, response_format="json"):
        return self.get(f"info/variation/populations/{species}/{population_name}", params=dict(callback=callback),
                        response_format=response_format, )

    def variation_populations(self, species: str, callback=None, filter=None, response_format="json"):
        return self.get(f"info/variation/populations/{species}", params=dict(callback=callback, filter=filter),
                        response_format=response_format, )

    def ld_id_get(self, id: str, population_name: str, species: str, attribs=None, callback=None, d_prime=None, r2=None,
                  window_size=None, response_format="json", ):
        return self.get(f"ld/{species}/{id}/{population_name}",
                        params=dict(attribs=attribs, callback=callback, d_prime=d_prime, r2=r2,
                                    window_size=window_size, ), response_format=response_format, )

    def ld_pairwise_get(self, id1: str, id2: str, species: str, callback=None, d_prime=None, population_name=None,
                        r2=None, response_format="json", ):
        return self.get(f"ld/{species}/pairwise/{id1}/{id2}",
                        params=dict(callback=callback, d_prime=d_prime, population_name=population_name, r2=r2),
                        response_format=response_format, )

    def ld_region_get(self, population_name: str, region: str, species: str, callback=None, d_prime=None, r2=None,
                      response_format="json", ):
        return self.get(f"ld/{species}/region/{region}/{population_name}",
                        params=dict(callback=callback, d_prime=d_prime, r2=r2), response_format=response_format, )

    @singledispatchmethod
    def lookup(self, id: str, callback=None, db_type=None, expand=None, format=None, mane=None, phenotypes=None,
               species=None, utr=None, response_format="json", ):
        return self.get(f"lookup/id/{id}",
                        params=dict(callback=callback, db_type=db_type, expand=expand, format=format, mane=mane,
                                    phenotypes=phenotypes, species=species, utr=utr, ),
                        response_format=response_format, )

    @lookup.register
    def _(self, id: list, callback=None, db_type=None, expand=None, format=None, object_type=None, species=None,
          response_format="json", ):
        return self.post(f"lookup/id", params=dict(callback=callback, db_type=db_type, expand=expand, format=format,
                                                   object_type=object_type, species=species, ),
                         response_format=response_format, json={"ids": id}, )

    @singledispatchmethod
    def symbol_lookup(self, symbol: str, species: str, callback=None, expand=None, format=None,
                      response_format="json", ):
        return self.get(f"lookup/symbol/{species}/{symbol}",
                        params=dict(callback=callback, expand=expand, format=format), response_format=response_format, )

    @symbol_lookup.register
    def _(self, symbol: list, species: str, callback=None, expand=None, format=None, response_format="json", ):
        return self.post(f"lookup/symbol/{species}/{symbol}",
                         params=dict(callback=callback, expand=expand, format=format), response_format=response_format,
                         json={"symbols": symbol}, )

    def assembly_cdna(self, id: str, region: str, callback=None, include_original_region=None, species=None,
                      response_format="json", ):
        return self.get(f"map/cdna/{id}/{region}",
                        params=dict(callback=callback, include_original_region=include_original_region,
                                    species=species, ), response_format=response_format, )

    def assembly_cds(self, id: str, region: str, callback=None, include_original_region=None, species=None,
                     response_format="json", ):
        return self.get(f"map/cds/{id}/{region}",
                        params=dict(callback=callback, include_original_region=include_original_region,
                                    species=species, ), response_format=response_format, )

    def assembly_map(self, asm_one: str, asm_two: str, region: str, species: str, callback=None, coord_system=None,
                     target_coord_system=None, response_format="json", ):
        return self.get(f"map/{species}/{asm_one}/{region}/{asm_two}",
                        params=dict(callback=callback, coord_system=coord_system,
                                    target_coord_system=target_coord_system, ), response_format=response_format, )

    def assembly_translation(self, id: str, region: str, callback=None, species=None, response_format="json"):
        return self.get(f"map/translation/{id}/{region}", params=dict(callback=callback, species=species),
                        response_format=response_format, )

    def ontology_ancestors(self, id: str, callback=None, ontology=None, response_format="json"):
        return self.get(f"ontology/ancestors/{id}", params=dict(callback=callback, ontology=ontology),
                        response_format=response_format, )

    def ontology_ancestors_chart(self, id: str, callback=None, ontology=None, response_format="json"):
        return self.get(f"ontology/ancestors/chart/{id}", params=dict(callback=callback, ontology=ontology),
                        response_format=response_format, )

    def ontology_descendants(self, id: str, callback=None, closest_term=None, ontology=None, subset=None,
                             zero_distance=None, response_format="json", ):
        return self.get(f"ontology/descendants/{id}",
                        params=dict(callback=callback, closest_term=closest_term, ontology=ontology, subset=subset,
                                    zero_distance=zero_distance, ), response_format=response_format, )

    def ontology_id(self, id: str, callback=None, relation=None, simple=None, response_format="json"):
        return self.get(f"ontology/id/{id}", params=dict(callback=callback, relation=relation, simple=simple),
                        response_format=response_format, )

    def ontology_name(self, name: str, callback=None, ontology=None, relation=None, simple=None,
                      response_format="json", ):
        return self.get(f"ontology/name/{name}",
                        params=dict(callback=callback, ontology=ontology, relation=relation, simple=simple),
                        response_format=response_format, )

    def taxonomy_classification(self, id: str, callback=None, response_format="json"):
        return self.get(f"taxonomy/classification/{id}", params=dict(callback=callback),
                        response_format=response_format, )

    def taxonomy_id(self, id: str, callback=None, simple=None, response_format="json"):
        return self.get(f"taxonomy/id/{id}", params=dict(callback=callback, simple=simple),
                        response_format=response_format, )

    def taxonomy_name(self, name: str, callback=None, response_format="json"):
        return self.get(f"taxonomy/name/{name}", params=dict(callback=callback), response_format=response_format, )

    def overlap_id(self, id: str, feature: str, biotype=None, callback=None, db_type=None, logic_name=None,
                   misc_set=None, object_type=None, so_term=None, species=None, species_set=None, variant_set=None,
                   response_format="json", ):
        return self.get(f"overlap/id/{id}",
                        params=dict(feature=feature, biotype=biotype, callback=callback, db_type=db_type,
                                    logic_name=logic_name, misc_set=misc_set, object_type=object_type, so_term=so_term,
                                    species=species, species_set=species_set, variant_set=variant_set, ),
                        response_format=response_format, )

    def overlap_region(self, region: str, feature: str, species: str, biotype=None, callback=None, db_type=None,
                       logic_name=None, misc_set=None, so_term=None, species_set=None, trim_downstream=None,
                       trim_upstream=None, variant_set=None, response_format="json", ):
        return self.get(f"overlap/region/{species}/{region}",
                        params=dict(feature=feature, biotype=biotype, callback=callback, db_type=db_type,
                                    logic_name=logic_name, misc_set=misc_set, so_term=so_term, species_set=species_set,
                                    trim_downstream=trim_downstream, trim_upstream=trim_upstream,
                                    variant_set=variant_set, ), response_format=response_format, )

    def overlap_translation(self, id: str, callback=None, db_type=None, feature=None, so_term=None, species=None,
                            type=None, response_format="json", ):
        return self.get(f"overlap/translation/{id}",
                        params=dict(callback=callback, db_type=db_type, feature=feature, so_term=so_term,
                                    species=species, type=type, ), response_format=response_format, )

    def phenotype_accession(self, accession: str, species: str, callback=None, include_children=None,
                            include_pubmed_id=None, include_review_status=None, source=None, response_format="json", ):
        return self.get(f"/phenotype/accession/{species}/{accession}",
                        params=dict(callback=callback, include_children=include_children,
                                    include_pubmed_id=include_pubmed_id, include_review_status=include_review_status,
                                    source=source, ), response_format=response_format, )

    def phenotype_gene(self, gene: str, species: str, callback=None, include_associated=None, include_overlap=None,
                       include_pubmed_id=None, include_review_status=None, include_submitter=None, non_specified=None,
                       trait=None, tumour=None, response_format="json", ):
        return self.get(f"/phenotype/gene/{species}/{gene}",
                        params=dict(callback=callback, include_associated=include_associated,
                                    include_overlap=include_overlap, include_pubmed_id=include_pubmed_id,
                                    include_review_status=include_review_status, include_submitter=include_submitter,
                                    non_specified=non_specified, trait=trait, tumour=tumour, ),
                        response_format=response_format, )

    def phenotype_region(self, region: str, species: str, callback=None, feature_type=None, include_pubmed_id=None,
                         include_review_status=None, include_submitter=None, non_specified=None, only_phenotypes=None,
                         trait=None, tumour=None, response_format="json", ):
        return self.get(f"/phenotype/region/{species}/{region}",
                        params=dict(callback=callback, feature_type=feature_type, include_pubmed_id=include_pubmed_id,
                                    include_review_status=include_review_status, include_submitter=include_submitter,
                                    non_specified=non_specified, only_phenotypes=only_phenotypes, trait=trait,
                                    tumour=tumour, ), response_format=response_format, )

    def phenotype_term(self, species: str, term: str, callback=None, include_children=None, include_pubmed_id=None,
                       include_review_status=None, source=None, response_format="json", ):
        return self.get(f"/phenotype/term/{species}/{term}",
                        params=dict(callback=callback, include_children=include_children,
                                    include_pubmed_id=include_pubmed_id, include_review_status=include_review_status,
                                    source=source, ), response_format=response_format, )

    def array(self, microarray: str, species: str, vendor: str, callback=None, response_format="json"):
        return self.get(f"regulatory/species/{species}/microarray/{microarray}/vendor/{vendor}",
                        params=dict(callback=callback), response_format=response_format, )

    def fetch_all_epigenomes(self, species: str, callback=None, response_format="json"):
        return self.get(f"regulatory/species/{species}/epigenome", params=dict(callback=callback),
                        response_format=response_format, )

    def get_binding_matrix(self, binding_matrix: str, species: str, callback=None, unit=None, response_format="json"):
        return self.get(f"species/{species}/binding_matrix/{binding_matrix}/",
                        params=dict(callback=callback, unit=unit), response_format=response_format, )

    def list_all_microarrays(self, species: str, callback=None, response_format="json"):
        return self.get(f"regulatory/species/{species}/microarray", params=dict(callback=callback),
                        response_format=response_format, )

    def probe(self, microarray: str, probe: str, species: str, callback=None, gene=None, transcripts=None,
              response_format="json", ):
        return self.get(f"regulatory/species/{species}/microarray/{microarray}/probe/{probe}",
                        params=dict(callback=callback, gene=gene, transcripts=transcripts),
                        response_format=response_format, )

    def probe_set(self, microarray: str, probe_set: str, species: str, callback=None, gene=None, transcripts=None,
                  response_format="json", ):
        return self.get(f"regulatory/species/{species}/microarray/{microarray}/probe_set/{probe_set}",
                        params=dict(callback=callback, gene=gene, transcripts=transcripts),
                        response_format=response_format, )

    def regulatory_id(self, id: str, species: str, activity=None, callback=None, response_format="json"):
        return self.get(f"regulatory/species/{species}/id/{id}", params=dict(activity=activity, callback=callback),
                        response_format=response_format, )

    @singledispatchmethod
    def sequence_id(self, id: str, callback=None, db_type=None, end=None, expand_3prime=None, expand_5prime=None,
                    format=None, mask=None, mask_feature=None, multiple_sequences=None, object_type=None, species=None,
                    start=None, type=None, response_format="json", ):
        return self.get(f"sequence/id/{id}",
                        params=dict(callback=callback, db_type=db_type, end=end, expand_3prime=expand_3prime,
                                    expand_5prime=expand_5prime, format=format, mask=mask, mask_feature=mask_feature,
                                    multiple_sequences=multiple_sequences, object_type=object_type, species=species,
                                    start=start, type=type, ), response_format=response_format, )

    @sequence_id.register
    def _(self, id: list, callback=None, db_type=None, end=None, expand_3prime=None, expand_5prime=None, format=None,
          mask=None, mask_feature=None, object_type=None, species=None, start=None, type=None,
          response_format="json", ):
        return self.post(f"sequence/id",
                         params=dict(callback=callback, db_type=db_type, end=end, expand_3prime=expand_3prime,
                                     expand_5prime=expand_5prime, format=format, mask=mask, mask_feature=mask_feature,
                                     object_type=object_type, species=species, start=start, type=type, ),
                         response_format=response_format, json={"ids": id}, )

    @singledispatchmethod
    def sequence_region(self, region: str, species: str, callback=None, coord_system=None, coord_system_version=None,
                        expand_3prime=None, expand_5prime=None, format=None, mask=None, mask_feature=None,
                        response_format="json", ):
        return self.get(f"sequence/region/{species}/{region}", params=dict(callback=callback, coord_system=coord_system,
                                                                           coord_system_version=coord_system_version,
                                                                           expand_3prime=expand_3prime,
                                                                           expand_5prime=expand_5prime, format=format,
                                                                           mask=mask, mask_feature=mask_feature, ),
                        response_format=response_format, )

    @sequence_region.register
    def _(self, region: list, species: str, callback=None, coord_system=None, coord_system_version=None,
          expand_3prime=None, expand_5prime=None, format=None, mask=None, mask_feature=None, response_format="json", ):
        return self.post(f"sequence/region/{species}", params=dict(callback=callback, coord_system=coord_system,
                                                                   coord_system_version=coord_system_version,
                                                                   expand_3prime=expand_3prime,
                                                                   expand_5prime=expand_5prime, format=format,
                                                                   mask=mask, mask_feature=mask_feature, ),
                         response_format=response_format, json={"regions": region}, )

    def transcript_haplotypes_get(self, id: str, species: str, aligned_sequences=None, callback=None, samples=None,
                                  sequence=None, response_format="json", ):
        return self.get(f"transcript_haplotypes/{species}/{id}",
                        params=dict(aligned_sequences=aligned_sequences, callback=callback, samples=samples,
                                    sequence=sequence, ), response_format=response_format, )

    @singledispatchmethod
    def vep_hgvs(self, hgvs_notation: str, species: str, AncestralAllele=None, Blosum62=None, CADD=None,
                 Conservation=None, DisGeNET=None, EVE=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None,
                 LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, Phenotypes=None, SpliceAI=None,
                 UTRAnnotator=None, ambiguous_hgvs=None, appris=None, callback=None, canonical=None, ccds=None,
                 dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None,
                 flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None,
                 mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None,
                 pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None,
                 shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
                 variant_class=None, vcf_string=None, xref_refseq=None, response_format="json", ):
        return self.get(f"vep/{species}/hgvs/{hgvs_notation}",
                        params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                                    Conservation=Conservation, DisGeNET=DisGeNET, EVE=EVE, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                    Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                    Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                                    ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback,
                                    canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance,
                                    domains=domains, failed=failed, flag_pick=flag_pick,
                                    flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                    ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane,
                                    merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                    per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                    pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                    refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                    transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                    uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                    xref_refseq=xref_refseq, ), response_format=response_format, )

    @vep_hgvs.register
    def _(self, hgvs_notation: list, species: str, AncestralAllele=None, Blosum62=None, CADD=None, DisGeNET=None,
          EVE=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None,
          MaxEntScan=None, NMD=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, ambiguous_hgvs=None,
          appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None,
          failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None,
          gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None,
          per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None, protein=None, refseq=None,
          shift_3prime=None, shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
          variant_class=None, vcf_string=None, xref_refseq=None, response_format="json", ):
        return self.post(f"vep/{species}/hgvs",
                         params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, DisGeNET=DisGeNET,
                                     EVE=EVE, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                     Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator,
                                     ambiguous_hgvs=ambiguous_hgvs, appris=appris, callback=callback,
                                     canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV, distance=distance,
                                     domains=domains, failed=failed, flag_pick=flag_pick,
                                     flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                     ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane,
                                     merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                     per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                     pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                     refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                     transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                     uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                     xref_refseq=xref_refseq, ), response_format=response_format,
                         json={"hgvs_notations": hgvs_notation}, )

    @singledispatchmethod
    def vep_id(self, id: str, species: str, AncestralAllele=None, Blosum62=None, CADD=None, Conservation=None,
               DisGeNET=None, EVE=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None,
               MaveDB=None, MaxEntScan=None, NMD=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None,
               callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None,
               failed=None, flag_pick=None, flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None,
               gencode_basic=None, hgvs=None, mane=None, merged=None, minimal=None, mirna=None, mutfunc=None,
               numbers=None, per_gene=None, pick=None, pick_allele=None, pick_allele_gene=None, pick_order=None,
               protein=None, refseq=None, shift_3prime=None, shift_genomic=None, transcript_id=None,
               transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None, xref_refseq=None,
               response_format="json", ):
        return self.get(f"vep/{species}/id/{id}",
                        params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                                    Conservation=Conservation, DisGeNET=DisGeNET, EVE=EVE, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                    Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                    Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris,
                                    callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                                    distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                                    flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                    ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane,
                                    merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                    per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                    pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                    refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                    transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                    uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                    xref_refseq=xref_refseq, ), response_format=response_format, )

    @vep_id.register
    def _(self, id: list, species: str, AncestralAllele=None, Blosum62=None, CADD=None, DisGeNET=None, EVE=None,
          GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None,
          NMD=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None,
          ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None,
          flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None,
          merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
          pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
          transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
          xref_refseq=None, response_format="json", ):
        return self.post(f"vep/{species}/id",
                         params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, DisGeNET=DisGeNET,
                                     EVE=EVE, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                     Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris,
                                     callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                                     distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                                     flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                     ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane,
                                     merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                     per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                     pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                     refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                     transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                     uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                     xref_refseq=xref_refseq, ), response_format=response_format, json={"ids": id}, )

    @singledispatchmethod
    def vep_region(self, region: str, allele: str, species: str, AncestralAllele=None, Blosum62=None, CADD=None,
                   Conservation=None, DisGeNET=None, EVE=None, GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None,
                   LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None, NMD=None, Phenotypes=None, SpliceAI=None,
                   UTRAnnotator=None, appris=None, callback=None, canonical=None, ccds=None, dbNSFP=None, dbscSNV=None,
                   distance=None, domains=None, failed=None, flag_pick=None, flag_pick_allele=None,
                   flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None, merged=None,
                   minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
                   pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None,
                   shift_genomic=None, transcript_id=None, transcript_version=None, tsl=None, uniprot=None,
                   variant_class=None, vcf_string=None, xref_refseq=None, response_format="json", ):
        return self.get(f"vep/{species}/region/{region}/{allele}/",
                        params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD,
                                    Conservation=Conservation, DisGeNET=DisGeNET, EVE=EVE, GO=GO,
                                    GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                    Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                    Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris,
                                    callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                                    distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                                    flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                    ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane,
                                    merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                    per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                    pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                    refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                    transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                    uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                    xref_refseq=xref_refseq, ), response_format=response_format, )

    @vep_region.register
    def _(self, region: list, species: str, AncestralAllele=None, Blosum62=None, CADD=None, DisGeNET=None, EVE=None,
          GO=None, GeneSplicer=None, Geno2MP=None, IntAct=None, LoF=None, Mastermind=None, MaveDB=None, MaxEntScan=None,
          NMD=None, Phenotypes=None, SpliceAI=None, UTRAnnotator=None, appris=None, callback=None, canonical=None,
          ccds=None, dbNSFP=None, dbscSNV=None, distance=None, domains=None, failed=None, flag_pick=None,
          flag_pick_allele=None, flag_pick_allele_gene=None, ga4gh_vrs=None, gencode_basic=None, hgvs=None, mane=None,
          merged=None, minimal=None, mirna=None, mutfunc=None, numbers=None, per_gene=None, pick=None, pick_allele=None,
          pick_allele_gene=None, pick_order=None, protein=None, refseq=None, shift_3prime=None, shift_genomic=None,
          transcript_id=None, transcript_version=None, tsl=None, uniprot=None, variant_class=None, vcf_string=None,
          xref_refseq=None, response_format="json", ):
        return self.post(f"vep/{species}/region",
                         params=dict(AncestralAllele=AncestralAllele, Blosum62=Blosum62, CADD=CADD, DisGeNET=DisGeNET,
                                     EVE=EVE, GO=GO, GeneSplicer=GeneSplicer, Geno2MP=Geno2MP, IntAct=IntAct, LoF=LoF,
                                     Mastermind=Mastermind, MaveDB=MaveDB, MaxEntScan=MaxEntScan, NMD=NMD,
                                     Phenotypes=Phenotypes, SpliceAI=SpliceAI, UTRAnnotator=UTRAnnotator, appris=appris,
                                     callback=callback, canonical=canonical, ccds=ccds, dbNSFP=dbNSFP, dbscSNV=dbscSNV,
                                     distance=distance, domains=domains, failed=failed, flag_pick=flag_pick,
                                     flag_pick_allele=flag_pick_allele, flag_pick_allele_gene=flag_pick_allele_gene,
                                     ga4gh_vrs=ga4gh_vrs, gencode_basic=gencode_basic, hgvs=hgvs, mane=mane,
                                     merged=merged, minimal=minimal, mirna=mirna, mutfunc=mutfunc, numbers=numbers,
                                     per_gene=per_gene, pick=pick, pick_allele=pick_allele,
                                     pick_allele_gene=pick_allele_gene, pick_order=pick_order, protein=protein,
                                     refseq=refseq, shift_3prime=shift_3prime, shift_genomic=shift_genomic,
                                     transcript_id=transcript_id, transcript_version=transcript_version, tsl=tsl,
                                     uniprot=uniprot, variant_class=variant_class, vcf_string=vcf_string,
                                     xref_refseq=xref_refseq, ), response_format=response_format,
                         json={"variants": region}, )

    @singledispatchmethod
    def variant_recoder(self, id: str, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None,
                        gencode_basic=None, minimal=None, var_synonyms=None, vcf_string=None, response_format="json", ):
        return self.get(f"variant_recoder/{species}/{id}",
                        params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                                    gencode_basic=gencode_basic, minimal=minimal, var_synonyms=var_synonyms,
                                    vcf_string=vcf_string, ), response_format=response_format, )

    @variant_recoder.register
    def _(self, id: list, species: str, callback=None, failed=None, fields=None, ga4gh_vrs=None, gencode_basic=None,
          minimal=None, var_synonyms=None, vcf_string=None, response_format="json", ):
        return self.post(f"variant_recoder/{species}",
                         params=dict(callback=callback, failed=failed, fields=fields, ga4gh_vrs=ga4gh_vrs,
                                     gencode_basic=gencode_basic, minimal=minimal, var_synonyms=var_synonyms,
                                     vcf_string=vcf_string, ), response_format=response_format, json={"ids": id}, )

    @singledispatchmethod
    def variation_id(self, id: str, species: str, callback=None, genotypes=None, genotyping_chips=None, phenotypes=None,
                     pops=None, population_genotypes=None, response_format="json", ):
        return self.get(f"variation/{species}/{id}",
                        params=dict(callback=callback, genotypes=genotypes, genotyping_chips=genotyping_chips,
                                    phenotypes=phenotypes, pops=pops, population_genotypes=population_genotypes, ),
                        response_format=response_format, )

    @variation_id.register
    def _(self, id: list, species: str, callback=None, genotypes=None, phenotypes=None, pops=None,
          population_genotypes=None, response_format="json", ):
        return self.post(f"variation/{species}/",
                         params=dict(callback=callback, genotypes=genotypes, phenotypes=phenotypes, pops=pops,
                                     population_genotypes=population_genotypes, ), response_format=response_format,
                         json={"ids": id}, )

    def variation_pmcid_get(self, pmcid: str, species: str, callback=None, response_format="json"):
        return self.get(f"variation/{species}/pmcid/{pmcid}", params=dict(callback=callback),
                        response_format=response_format, )

    def variation_pmid_get(self, pmid: str, species: str, callback=None, response_format="json"):
        return self.get(f"variation/{species}/pmid/{pmid}", params=dict(callback=callback),
                        response_format=response_format, )

    def beacon_get(self, callback=None, response_format="json"):
        return self.get(f"ga4gh/beacon", params=dict(callback=callback), response_format=response_format)

    def beacon_query_get(self, response_format="json", **kwargs, ):
        return self.get(f"ga4gh/beacon/query", params=dict(**kwargs), response_format=response_format)

    def beacon_query_post(self, response_format="json", **kwargs):
        return self.post(f"ga4gh/beacon/query", params={}, response_format=response_format, json=dict(**kwargs))

    def features_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/features/{id}", params=dict(callback=callback), response_format=response_format)

    def features_post(self, response_format="json", **kwargs):
        return self.post(f"ga4gh/features/search", params={}, response_format=response_format, json=dict(**kwargs))

    def gacallSet(self, response_format="json", **kwargs):
        return self.post(f"ga4gh/callsets/search", params={}, response_format=response_format, json=dict(**kwargs))

    def gacallset_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/callsets/{id}", params=dict(callback=callback), response_format=response_format)

    def gadataset(self, callback=None, pageSize=None, pageToken=None, response_format="json"):
        return self.post(f"ga4gh/datasets/search", params=dict(callback=callback),
                         json=dict(pageSize=pageSize, pageToken=pageToken), response_format=response_format, )

    def gadataset_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/datasets/{id}", params=dict(callback=callback), response_format=response_format, )

    def gafeatureset(self, datasetId: str, callback=None, pageSize=None, pageToken=None, response_format="json"):
        return self.post(f"ga4gh/featuresets/search", params=dict(callback=callback),
                         json=dict(datasetId=datasetId, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format, )

    def gafeatureset_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/featuresets/{id}", params=dict(callback=callback), response_format=response_format, )

    def gavariant_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/variants/{id}", params=dict(callback=callback), response_format=response_format, )

    def gavariantannotations(self, variantAnnotationSetId: str, callback=None, effects=None, end=None, pageSize=None,
                             pageToken=None, referenceId=None, referenceName=None, start=None,
                             response_format="json", ):
        return self.post(f"ga4gh/variantannotations/search", params=dict(callback=callback),
                         json=dict(variantAnnotationSetId=variantAnnotationSetId, effects=effects, end=end,
                                   pageSize=pageSize, pageToken=pageToken, referenceId=referenceId,
                                   referenceName=referenceName, start=start, ), response_format=response_format, )

    def gavariants(self, end: str, referenceName: str, start: str, variantSetId: str, callSetIds=None, callback=None,
                   pageSize=None, pageToken=None, response_format="json", ):
        return self.post(f"ga4gh/variants/search", params=dict(callback=callback),
                         json=dict(pageSize=pageSize, pageToken=pageToken, callSetIds=callSetIds, end=end,
                                   referenceName=referenceName, start=start, variantSetId=variantSetId, ),
                         response_format=response_format, )

    def gavariantset(self, datasetId: str, callback=None, pageSize=None, pageToken=None, response_format="json"):
        return self.post(f"ga4gh/variantsets/search", params=dict(callback=callback),
                         json=dict(datasetId=datasetId, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format, )

    def gavariantset_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/variantsets/{id}", params=dict(callback=callback), response_format=response_format, )

    def references(self, referenceSetId: str, accession=None, callback=None, md5checksum=None, pageSize=None,
                   pageToken=None, response_format="json", ):
        return self.post(f"ga4gh/references/search", params=dict(callback=callback),
                         json=dict(accession=accession, referenceSetId=referenceSetId, md5checksum=md5checksum,
                                   pageSize=pageSize, pageToken=pageToken, ), response_format=response_format, )

    def references_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/references/{id}", params=dict(callback=callback), response_format=response_format, )

    def referenceSets(self, accession=None, callback=None, pageSize=None, pageToken=None, response_format="json"):
        return self.post(f"ga4gh/referencesets/search", params=dict(callback=callback),
                         json=dict(accession=accession, pageSize=pageSize, pageToken=pageToken, ),
                         response_format=response_format, )

    def referenceSets_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/referencesets/{id}", params=dict(callback=callback), response_format=response_format, )

    def VariantAnnotationSet(self, variantSetId: str, callback=None, pageSize=None, pageToken=None,
                             response_format="json", ):
        return self.post(f"ga4gh/variantannotationsets/search", params=dict(callback=callback),
                         json=dict(variantSetId=variantSetId, pageSize=pageSize, pageToken=pageToken),
                         response_format=response_format, )

    def VariantAnnotationSet_id(self, id: str, callback=None, response_format="json"):
        return self.get(f"ga4gh/variantannotationsets/{id}", params=dict(callback=callback),
                        response_format=response_format, )


if __name__ == "__main__":
    print(archive("ENSG00000157764"))
    print(archive(["ENSG00000157764", "ENSG00000248378"]))
    print(genomic_alignment_region("X:1000000..1000100", "human"))
    print(homology_ensemblgene("ENSG00000173786"))
    print(homology_species_gene_id("ENSG00000173786", "human"))
    print(homology_symbol("human", "BRCA2"))
    print(xref_external("human", "BRCA2"))
    print(xref_id("ENSG00000157764"))
    print(xref_name("BRCA2", "human"))
    print(analysis("human"))
    print(assembly_info("human"))
    print(assembly_stats("X", "human"))
    print(biotypes("human"))
    print(biotypes_groups(group="coding", object_type="gene"))
    print(biotypes_name("protein_coding", object_type="gene"))
    print(compara_methods())
    print(compara_species_sets("LASTZ_NET"))
    print(comparas())
    print(data())
    print(external_dbs("human"))
    print(ping())
    print(rest())
    print(software())
    print(species())
    print(variation("human"))
    print(variation_consequence_types())
    print(variation_population_name("1000GENOMES:phase_3:ASW", "human"))
    print(variation_populations("human"))
    print(ld_id_get("rs1333049", "1000GENOMES:phase_3:GBR", "human"))
    print(ld_pairwise_get("rs1333049", "rs1333048", "human"))
    print(ld_region_get("1000GENOMES:phase_3:KHV", "6:25837556..25843455", "human"))
    print(lookup("ENSG00000157764", species="human"))
    print(lookup(["ENSG00000157764", "ENSG00000248378"], species="human"))
    print(symbol_lookup("BRCA2", "human"))
    print(symbol_lookup(["BRCA2", "BRCA1"], "human"))
    print(assembly_cdna("ENST00000288602", "100..300"))
    print(assembly_cds("ENST00000288602", "1..1000"))
    print(assembly_map("GRCh38", "GRCh37", "X:1000000-1001000", "human"))
    print(assembly_translation("ENSP00000288602", "100..300"))
    print(ontology_ancestors("GO:0005667"))
    print(ontology_ancestors_chart("GO:0005667"))
    print(ontology_descendants("GO:0005667"))
    print(ontology_id("GO:0005667"))
    print(ontology_name("transcription factor complex"))
    print(taxonomy_classification("9606"))
    print(taxonomy_id("9606"))
    print(taxonomy_name("human"))
    print(overlap_id("ENSG00000157764", "gene"))
    print(overlap_region(species="human", region="7:140424943-140624564", feature="gene"))
    print(overlap_translation("ENSP00000288602"))
    print(phenotype_accession(species="human", accession="EFO:0003900"))
    print(phenotype_gene(species="human", gene="BRCA2"))
    print(phenotype_region(species="human", region="9:22125500-22136000"))
    print(phenotype_term(species="human", term="coffee consumption"))
    print(array(species="human", microarray="HumanWG_6_V3", vendor="illumina"))
    print(fetch_all_epigenomes("human"))
    print(get_binding_matrix(species="human", binding_matrix="ENSPFM0001"))
    print(list_all_microarrays("human"))
    print(probe(species="human", microarray="HumanWG_6_V3", probe="ILMN_1910180"))
    print(probe_set(species="human", microarray="HG-U133_Plus_2", probe_set="202820_at"))
    print(regulatory_id(species="human", id="ENSR00000082023"))
    print(sequence_id("ENSG00000157764", species="human"))
    print(sequence_id(["ENSG00000157764", "ENSG00000248378"], species="human"))
    print(sequence_region("X:1000000..1000100", species="human"))
    print(sequence_region(["X:1000000..1000100:1", "ABBA01004489.1:1..100"], species="human"))
    print(transcript_haplotypes_get(id="ENST00000288602", species="human"))
    print(vep_hgvs("LRG_199t1:c.1A>T", species="human"))
    print(vep_hgvs(["AGT:c.803T>C", "9:g.22125503G>C"], species="human"))
    print(vep_id("rs116035550", species="human"))
    print(vep_id(["rs116035550", "COSM476"], species="human"))
    print(vep_region("9:22125503-22125502:1", allele="C", species="human"))
    print(vep_region(["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ."], species="human", ))
    print(variant_recoder("rs116035550", "human"))
    print(variant_recoder(["rs116035550", "rs1042779"], "human"))
    print(variation_id(["rs116035550", "COSM476"], "human"))
    print(variation_id("rs116035550", "human"))
    print(variation_pmcid_get("PMC5002951", "human"))
    print(variation_pmid_get("26318936", "human"))
    print(beacon_get())
    print(beacon_query_get(assemblyId="GRCh37", start=22125503, alternateBases="C", referenceName="9",
                           referenceBases="G", ))
    print(beacon_query_post(assemblyId="GRCh37", start=22125503, alternateBases="C", referenceName="9",
                            referenceBases="G", includeResultsetResponses=None, ))
    print(features_id("ENST00000381657.2"))
    print(features_post(parentId="ENST00000381657.2", pageSize=2, featureSetId="", featureTypes=["cds"], start=197859,
                        end=220023, referenceName="X"))
    print(gacallSet(variantSetId=3, pageSize=2))
    print(gacallset_id(id="3:NA19777"))
    print(gadataset(pageSize=3))
    print(gadataset_id(id="6e340c4d1e333c7a676b1710d2e3953c"))
    print(gafeatureset(datasetId="Ensembl", pageSize=2))
    print(gafeatureset_id(id="Ensembl"))
    print(gavariant_id(id="3:rs1333049"))
    print(gavariantannotations(pageSize=2, variantAnnotationSetId="Ensembl",
                               referenceId="a718acaa6135fdca8357d5bfe94211dd", start=25617400, end=25617500))
    print(
        gavariants(variantSetId=3, callSetIds=["3:NA19777", "3:HG01242", "3:HG01142"], referenceName=22, start=17190024,
                   end=17671934, pageToken="", pageSize=3))
    print(gavariantset(datasetId="6e340c4d1e333c7a676b1710d2e3953c", pageToken="", pageSize=2))
    print(gavariantset_id(3))
    print(references(referenceSetId="GRCh37.p13", pageSize=10))
    print(references_id("a718acaa6135fdca8357d5bfe94211dd"))
    print(referenceSets())
    print(referenceSets_id("GRCh37.p13"))
    print(VariantAnnotationSet(variantSetId="Ensembl"))
    print(VariantAnnotationSet_id("Ensembl"))
    ensembl = Ensembl()
    print(ensembl.archive("ENSG00000157764"))
    print(ensembl.archive(["ENSG00000157764", "ENSG00000248378"]))
    print(ensembl.genomic_alignment_region("X:1000000..1000100", "human"))
    print(ensembl.homology_ensemblgene("ENSG00000173786"))
    print(ensembl.homology_species_gene_id("ENSG00000173786", "human"))
    print(ensembl.homology_symbol("human", "BRCA2"))
    print(ensembl.xref_external("human", "BRCA2"))
    print(ensembl.xref_id("ENSG00000157764"))
    print(ensembl.xref_name("BRCA2", "human"))
    print(ensembl.analysis("human"))
    print(ensembl.assembly_info("human"))
    print(ensembl.assembly_stats("X", "human"))
    print(ensembl.biotypes("human"))
    print(ensembl.biotypes_groups(group="coding", object_type="gene"))
    print(ensembl.biotypes_name("protein_coding", object_type="gene"))
    print(ensembl.compara_methods())
    print(ensembl.compara_species_sets("LASTZ_NET"))
    print(ensembl.comparas())
    print(ensembl.data())
    print(ensembl.external_dbs("human"))
    print(ensembl.ping())
    print(ensembl.rest())
    print(ensembl.software())
    print(ensembl.species())
    print(ensembl.variation("human"))
    print(ensembl.variation_consequence_types())
    print(ensembl.variation_population_name("1000GENOMES:phase_3:ASW", "human"))
    print(ensembl.variation_populations("human"))
    print(ensembl.ld_id_get("rs1333049", "1000GENOMES:phase_3:GBR", "human"))
    print(ensembl.ld_pairwise_get("rs1333049", "rs1333048", "human"))
    print(ensembl.ld_region_get("1000GENOMES:phase_3:KHV", "6:25837556..25843455", "human"))
    print(ensembl.lookup("ENSG00000157764", species="human"))
    print(ensembl.lookup(["ENSG00000157764", "ENSG00000248378"], species="human"))
    print(ensembl.symbol_lookup("BRCA2", "human"))
    print(ensembl.symbol_lookup(["BRCA2", "BRCA1"], "human"))
    print(ensembl.assembly_cdna("ENST00000288602", "100..300"))
    print(ensembl.assembly_cds("ENST00000288602", "1..1000"))
    print(ensembl.assembly_map("GRCh38", "GRCh37", "X:1000000-1001000", "human"))
    print(ensembl.assembly_translation("ENSP00000288602", "100..300"))
    print(ensembl.ontology_ancestors("GO:0005667"))
    print(ensembl.ontology_ancestors_chart("GO:0005667"))
    print(ensembl.ontology_descendants("GO:0005667"))
    print(ensembl.ontology_id("GO:0005667"))
    print(ensembl.ontology_name("transcription factor complex"))
    print(ensembl.taxonomy_classification("9606"))
    print(ensembl.taxonomy_id("9606"))
    print(ensembl.taxonomy_name("human"))
    print(ensembl.overlap_id("ENSG00000157764", "gene"))
    print(ensembl.overlap_region(species="human", region="7:140424943-140624564", feature="gene"))
    print(ensembl.overlap_translation("ENSP00000288602"))
    print(ensembl.phenotype_accession(species="human", accession="EFO:0003900"))
    print(ensembl.phenotype_gene(species="human", gene="BRCA2"))
    print(ensembl.phenotype_region(species="human", region="9:22125500-22136000"))
    print(ensembl.phenotype_term(species="human", term="coffee consumption"))
    print(ensembl.array(species="human", microarray="HumanWG_6_V3", vendor="illumina"))
    print(ensembl.fetch_all_epigenomes("human"))
    print(ensembl.get_binding_matrix(species="human", binding_matrix="ENSPFM0001"))
    print(ensembl.list_all_microarrays("human"))
    print(ensembl.probe(species="human", microarray="HumanWG_6_V3", probe="ILMN_1910180"))
    print(ensembl.probe_set(species="human", microarray="HG-U133_Plus_2", probe_set="202820_at"))
    print(ensembl.regulatory_id(species="human", id="ENSR00000082023"))
    print(ensembl.sequence_id("ENSG00000157764", species="human"))
    print(ensembl.sequence_id(["ENSG00000157764", "ENSG00000248378"], species="human"))
    print(ensembl.sequence_region("X:1000000..1000100", species="human"))
    print(ensembl.sequence_region(["X:1000000..1000100:1", "ABBA01004489.1:1..100"], species="human"))
    print(ensembl.transcript_haplotypes_get(id="ENST00000288602", species="human"))
    print(ensembl.vep_hgvs("LRG_199t1:c.1A>T", species="human"))
    print(ensembl.vep_hgvs(["AGT:c.803T>C", "9:g.22125503G>C"], species="human"))
    print(ensembl.vep_id("rs116035550", species="human"))
    print(ensembl.vep_id(["rs116035550", "COSM476"], species="human"))
    print(ensembl.vep_region("9:22125503-22125502:1", "C", "human"))
    print(ensembl.vep_region(["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ."], "human", ))
    print(ensembl.variant_recoder("rs116035550", "human"))
    print(ensembl.variant_recoder(["rs116035550", "rs1042779"], "human"))
    print(ensembl.variation_id(["rs116035550", "COSM476"], "human"))
    print(ensembl.variation_id("rs116035550", "human"))
    print(ensembl.variation_pmcid_get("PMC5002951", "human"))
    print(ensembl.variation_pmid_get("26318936", "human"))
    print(ensembl.beacon_get())
    print(ensembl.beacon_query_get(assemblyId="GRCh37", start=22125503, alternateBases="C", referenceName="9",
                                   referenceBases="G", ))
    print(ensembl.beacon_query_post(assemblyId="GRCh37", start=22125503, alternateBases="C", referenceName="9",
                                    referenceBases="G", includeResultsetResponses=None, ))
    print(ensembl.features_id("ENST00000381657.2"))
    print(ensembl.features_post(parentId="ENST00000381657.2", pageSize=2, featureSetId="", featureTypes=["cds"],
                                start=197859, end=220023, referenceName="X"))
    print(ensembl.gacallSet(variantSetId=3, pageSize=2))
    print(ensembl.gacallset_id(id="3:NA19777"))
    print(ensembl.gadataset(pageSize=3))
    print(ensembl.gadataset_id(id="6e340c4d1e333c7a676b1710d2e3953c"))
    print(ensembl.gafeatureset(datasetId="Ensembl", pageSize=2))
    print(ensembl.gafeatureset_id(id="Ensembl"))
    print(ensembl.gavariant_id(id="3:rs1333049"))
    print(ensembl.gavariantannotations(pageSize=2, variantAnnotationSetId="Ensembl",
                                       referenceId="a718acaa6135fdca8357d5bfe94211dd", start=25617400, end=25617500))
    print(ensembl.gavariants(variantSetId=3, callSetIds=["3:NA19777", "3:HG01242", "3:HG01142"], referenceName=22,
                             start=17190024, end=17671934, pageToken="", pageSize=3))
    print(ensembl.gavariantset(datasetId="6e340c4d1e333c7a676b1710d2e3953c", pageToken="", pageSize=2))
    print(ensembl.gavariantset_id(3))
    print(ensembl.references(referenceSetId="GRCh37.p13", pageSize=10))
    print(ensembl.references_id("a718acaa6135fdca8357d5bfe94211dd"))
    print(ensembl.referenceSets())
    print(ensembl.referenceSets_id("GRCh37.p13"))
    print(ensembl.VariantAnnotationSet(variantSetId="Ensembl"))
    print(ensembl.VariantAnnotationSet_id("Ensembl"))
